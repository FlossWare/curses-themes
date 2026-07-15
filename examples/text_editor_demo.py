#!/usr/bin/env python3
"""
Themed Text Editor Demo - Interactive TUI text editor with theme support.

This intermediate example demonstrates building a practical text editor interface
with the curses-themes library. It showcases multi-window layouts, status bars,
line numbers, file browser, and runtime theme switching.

Features demonstrated:
    - Multi-window layout with menu bar, editor area, and status bar
    - Line numbers with themed colors
    - File browser sidebar with selection highlighting
    - Status bar showing cursor position, file info, and current theme
    - Runtime theme switching with hotkeys (F1-F8)
    - Command palette with semantic color feedback (success/error messages)
    - Scrolling text area with viewport management
    - Modal dialogs for save/open operations using draw_box
    - Component colors: borders, selections, text input

Controls:
    F1-F8: Switch between themes (default, dark, light, TI-99/4A, TRS-80, DOS, dBASE III, dBASE IV)
    Ctrl+O: Open file browser
    Ctrl+S: Save file
    Ctrl+N: New file
    Ctrl+Q: Quit
    Arrow keys: Navigate text
    Page Up/Down: Scroll by page
    Home/End: Jump to line start/end
    TAB: Switch between editor and file browser
    ESC: Close dialogs/deselect

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.

Usage:
    python3 text_editor_demo.py [filename]

    Example:
        python3 text_editor_demo.py myfile.txt
"""

import curses
import os
import sys
from typing import List, Optional, Tuple

# Add parent directory to path to allow running from examples directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from curses_themes import ThemeManager


class TextBuffer:
    """Manages the text content and cursor position."""

    def __init__(self, filename: Optional[str] = None):
        """
        Initialize text buffer.

        Args:
            filename: Optional file to load
        """
        self.filename = filename or "Untitled"
        self.lines: List[str] = [""]
        self.cursor_row = 0
        self.cursor_col = 0
        self.modified = False

        if filename and os.path.exists(filename):
            self.load_file(filename)

    def load_file(self, filename: str) -> Tuple[bool, str]:
        """
        Load file into buffer.

        Args:
            filename: Path to file

        Returns:
            Tuple of (success, message)
        """
        try:
            with open(filename) as f:
                self.lines = f.read().splitlines() or [""]
            self.filename = filename
            self.cursor_row = 0
            self.cursor_col = 0
            self.modified = False
            return True, f"Loaded {filename}"
        except Exception as e:
            return False, f"Error loading file: {e}"

    def save_file(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """
        Save buffer to file.

        Args:
            filename: Optional new filename

        Returns:
            Tuple of (success, message)
        """
        save_to = filename or self.filename
        if save_to == "Untitled":
            return False, "Please specify a filename"

        try:
            with open(save_to, "w") as f:
                f.write("\n".join(self.lines))
            self.filename = save_to
            self.modified = False
            return True, f"Saved {save_to}"
        except Exception as e:
            return False, f"Error saving file: {e}"

    def insert_char(self, char: str) -> None:
        """Insert character at cursor position."""
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = (
            line[: self.cursor_col] + char + line[self.cursor_col :]
        )
        self.cursor_col += 1
        self.modified = True

    def delete_char(self) -> None:
        """Delete character before cursor (backspace)."""
        if self.cursor_col > 0:
            line = self.lines[self.cursor_row]
            self.lines[self.cursor_row] = (
                line[: self.cursor_col - 1] + line[self.cursor_col :]
            )
            self.cursor_col -= 1
            self.modified = True
        elif self.cursor_row > 0:
            # Join with previous line
            prev_line = self.lines[self.cursor_row - 1]
            curr_line = self.lines[self.cursor_row]
            self.lines[self.cursor_row - 1] = prev_line + curr_line
            del self.lines[self.cursor_row]
            self.cursor_row -= 1
            self.cursor_col = len(prev_line)
            self.modified = True

    def insert_newline(self) -> None:
        """Insert newline at cursor position."""
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = line[: self.cursor_col]
        self.lines.insert(self.cursor_row + 1, line[self.cursor_col :])
        self.cursor_row += 1
        self.cursor_col = 0
        self.modified = True

    def move_cursor(self, dy: int, dx: int) -> None:
        """
        Move cursor by delta.

        Args:
            dy: Vertical delta
            dx: Horizontal delta
        """
        # Move vertically
        self.cursor_row = max(0, min(len(self.lines) - 1, self.cursor_row + dy))

        # Move horizontally
        max_col = len(self.lines[self.cursor_row])
        self.cursor_col = max(0, min(max_col, self.cursor_col + dx))


class FileBrowser:
    """Simple file browser for opening files."""

    def __init__(self, path: str = "."):
        """
        Initialize file browser.

        Args:
            path: Starting directory path
        """
        self.path = os.path.abspath(path)
        self.files: List[str] = []
        self.selected = 0
        self.scroll_offset = 0
        self.refresh_files()

    def refresh_files(self) -> None:
        """Refresh file list from current directory."""
        try:
            entries = os.listdir(self.path)
            self.files = (
                [".."]
                + sorted(
                    [f for f in entries if os.path.isdir(os.path.join(self.path, f))],
                    key=str.lower,
                )
                + sorted(
                    [f for f in entries if os.path.isfile(os.path.join(self.path, f))],
                    key=str.lower,
                )
            )
            self.selected = 0
            self.scroll_offset = 0
        except Exception:
            self.files = [".."]

    def move_selection(self, delta: int) -> None:
        """
        Move selection by delta.

        Args:
            delta: Amount to move selection
        """
        self.selected = max(0, min(len(self.files) - 1, self.selected + delta))

    def get_selected_path(self) -> str:
        """Get absolute path of selected file."""
        if not self.files:
            return self.path
        return os.path.join(self.path, self.files[self.selected])

    def enter_selected(self) -> Optional[str]:
        """
        Enter selected directory or return selected file.

        Returns:
            File path if file selected, None if directory entered
        """
        if not self.files:
            return None

        selected_path = self.get_selected_path()

        if os.path.isdir(selected_path):
            self.path = os.path.abspath(selected_path)
            self.refresh_files()
            return None
        else:
            return selected_path


class TextEditor:
    """Main text editor application."""

    # Theme names mapped to F-keys
    THEMES = [
        "default",  # F1
        "dark",  # F2
        "light",  # F3
        "ti-99-4a",  # F4
        "trs-80",  # F5
        "dos",  # F6
        "dbase-iii",  # F7
        "dbase-iv",  # F8
    ]

    def __init__(self, stdscr, filename: Optional[str] = None):
        """
        Initialize text editor.

        Args:
            stdscr: Curses window
            filename: Optional file to load
        """
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()

        # Initialize components
        self.buffer = TextBuffer(filename)
        self.browser = FileBrowser()

        # UI state
        self.current_theme_index = 0
        self.theme = ThemeManager.load(self.THEMES[self.current_theme_index])
        self.message = ""
        self.message_color = None
        self.show_browser = False
        self.browser_focused = False
        self.scroll_row = 0

        # Configure curses
        curses.curs_set(1)  # Show cursor
        stdscr.keypad(True)

        # Apply initial theme
        self.theme.apply(stdscr)

    def switch_theme(self, theme_index: int) -> None:
        """
        Switch to theme by index.

        Args:
            theme_index: Index into THEMES list
        """
        if 0 <= theme_index < len(self.THEMES):
            self.current_theme_index = theme_index
            self.theme = ThemeManager.load(self.THEMES[theme_index])
            self.theme.apply(self.stdscr)
            self.set_message(
                f"Theme: {self.THEMES[theme_index]}", self.theme.colors.info
            )

    def set_message(self, msg: str, color: Optional[int] = None) -> None:
        """
        Set status message.

        Args:
            msg: Message text
            color: Optional color pair number
        """
        self.message = msg
        self.message_color = color

    def draw_menu_bar(self) -> None:
        """Draw the top menu bar."""
        menu_items = [
            "^N New",
            "^O Open",
            "^S Save",
            "^Q Quit",
            "F1-F8 Themes",
            "TAB Switch",
        ]
        menu_text = "  ".join(menu_items)

        try:
            self.stdscr.addstr(0, 0, " " * self.width, self.theme.components.button)
            self.stdscr.addstr(
                0, 2, menu_text[: self.width - 4], self.theme.components.button
            )
        except curses.error:
            pass

    def draw_status_bar(self) -> None:
        """Draw the bottom status bar."""
        # Left side: file info
        mod_indicator = "*" if self.buffer.modified else " "
        left_text = f" {self.buffer.filename}{mod_indicator}"

        # Center: cursor position
        center_text = (
            f"Line {self.buffer.cursor_row + 1}, Col {self.buffer.cursor_col + 1}"
        )

        # Right side: theme name
        right_text = f"{self.THEMES[self.current_theme_index]} "

        status_y = self.height - 2

        try:
            # Draw status bar background
            self.stdscr.addstr(
                status_y, 0, " " * self.width, self.theme.components.button_focused
            )

            # Draw left text
            self.stdscr.addstr(
                status_y,
                0,
                left_text[: self.width // 3],
                self.theme.components.button_focused,
            )

            # Draw center text
            center_x = (self.width - len(center_text)) // 2
            if center_x > 0:
                self.stdscr.addstr(
                    status_y,
                    center_x,
                    center_text,
                    self.theme.components.button_focused,
                )

            # Draw right text
            right_x = self.width - len(right_text)
            if right_x > 0:
                self.stdscr.addstr(
                    status_y, right_x, right_text, self.theme.components.button_focused
                )
        except curses.error:
            pass

    def draw_message_bar(self) -> None:
        """Draw the message/command bar."""
        msg_y = self.height - 1
        color = self.message_color or self.theme.colors.foreground

        try:
            self.stdscr.addstr(msg_y, 0, " " * self.width, color)
            if self.message:
                self.stdscr.addstr(msg_y, 2, self.message[: self.width - 4], color)
        except curses.error:
            pass

    def draw_line_numbers(self, start_row: int, num_rows: int) -> int:
        """
        Draw line numbers for visible rows.

        Args:
            start_row: First line number to draw
            num_rows: Number of rows to draw

        Returns:
            Width of line number column
        """
        max_line = len(self.buffer.lines)
        num_width = len(str(max_line)) + 1

        for i in range(num_rows):
            line_num = start_row + i
            if line_num < len(self.buffer.lines):
                num_str = f"{line_num + 1:>{num_width - 1}} "
                try:
                    self.stdscr.addstr(2 + i, 0, num_str, self.theme.colors.accent)
                except curses.error:
                    pass

        return num_width

    def draw_editor(self) -> None:
        """Draw the main editor area."""
        # Calculate editor area dimensions
        editor_top = 2  # Below menu bar + separator
        editor_bottom = self.height - 2  # Above status bar
        editor_height = editor_bottom - editor_top

        # Determine sidebar width
        sidebar_width = 20 if self.show_browser else 0

        # Adjust scroll to keep cursor visible
        self.scroll_row = min(self.scroll_row, self.buffer.cursor_row)
        if self.buffer.cursor_row >= self.scroll_row + editor_height:
            self.scroll_row = self.buffer.cursor_row - editor_height + 1

        # Draw line numbers
        line_num_width = self.draw_line_numbers(self.scroll_row, editor_height)

        # Draw text content
        text_start_x = line_num_width + 1
        text_width = self.width - text_start_x - sidebar_width

        for i in range(editor_height):
            row_num = self.scroll_row + i
            y_pos = editor_top + i

            if row_num < len(self.buffer.lines):
                line = self.buffer.lines[row_num]
                # Truncate or pad line to fit
                display_line = line[:text_width].ljust(text_width)

                try:
                    self.stdscr.addstr(
                        y_pos, text_start_x, display_line, self.theme.colors.foreground
                    )
                except curses.error:
                    pass

        # Draw vertical separator for line numbers
        for i in range(editor_height):
            try:
                self.stdscr.addstr(
                    editor_top + i, line_num_width, "|", self.theme.components.border
                )
            except curses.error:
                pass

        # Position cursor
        if self.scroll_row <= self.buffer.cursor_row < self.scroll_row + editor_height:
            cursor_y = editor_top + (self.buffer.cursor_row - self.scroll_row)
            cursor_x = text_start_x + self.buffer.cursor_col

            if cursor_x < self.width - sidebar_width:
                try:
                    self.stdscr.move(cursor_y, cursor_x)
                except curses.error:
                    pass

    def draw_file_browser(self) -> None:
        """Draw the file browser sidebar."""
        if not self.show_browser:
            return

        browser_width = 20
        browser_x = self.width - browser_width
        browser_top = 2
        browser_bottom = self.height - 2
        browser_height = browser_bottom - browser_top

        # Draw browser box
        self.theme.draw_box(
            self.stdscr,
            browser_top - 1,
            browser_x - 1,
            browser_height + 2,
            browser_width + 1,
            title="Files",
            color_pair=self.theme.components.border
            if not self.browser_focused
            else self.theme.colors.primary,
        )

        # Adjust browser scroll
        self.browser.scroll_offset = min(
            self.browser.scroll_offset, self.browser.selected
        )
        if self.browser.selected >= self.browser.scroll_offset + browser_height:
            self.browser.scroll_offset = self.browser.selected - browser_height + 1

        # Draw file list
        for i in range(browser_height):
            file_idx = self.browser.scroll_offset + i
            if file_idx < len(self.browser.files):
                filename = self.browser.files[file_idx]

                # Truncate filename to fit
                display_name = filename[: browser_width - 2]

                # Determine if this is a directory
                is_dir = os.path.isdir(os.path.join(self.browser.path, filename))
                if is_dir:
                    display_name = f"[{display_name}]"

                # Highlight selected file
                if file_idx == self.browser.selected:
                    color = self.theme.components.selection
                else:
                    color = self.theme.colors.foreground

                try:
                    self.stdscr.addstr(
                        browser_top + i,
                        browser_x,
                        display_name[: browser_width - 1],
                        color,
                    )
                except curses.error:
                    pass

    def draw(self) -> None:
        """Draw the complete editor interface."""
        self.stdscr.clear()

        # Draw components
        self.draw_menu_bar()

        # Draw horizontal separator
        try:
            self.stdscr.addstr(1, 0, "-" * self.width, self.theme.components.border)
        except curses.error:
            pass

        self.draw_editor()
        self.draw_file_browser()
        self.draw_status_bar()
        self.draw_message_bar()

        self.stdscr.refresh()

    def handle_key(self, key: int) -> bool:
        """
        Handle keyboard input.

        Args:
            key: Key code from getch()

        Returns:
            False to quit, True to continue
        """
        # Theme switching (F1-F8)
        if curses.KEY_F1 <= key <= curses.KEY_F8:
            self.switch_theme(key - curses.KEY_F1)
            return True

        # Quit (Ctrl+Q)
        if key == ord("\x11"):  # Ctrl+Q
            if self.buffer.modified:
                self.set_message(
                    "Unsaved changes! Press Ctrl+Q again to quit",
                    self.theme.colors.warning,
                )
                # Simple confirmation: require two Ctrl+Q in a row
                self.stdscr.refresh()
                next_key = self.stdscr.getch()
                if next_key == ord("\x11"):
                    return False
                return True
            return False

        # Save (Ctrl+S)
        if key == ord("\x13"):  # Ctrl+S
            success, msg = self.buffer.save_file()
            color = self.theme.colors.success if success else self.theme.colors.error
            self.set_message(msg, color)
            return True

        # New file (Ctrl+N)
        if key == ord("\x0e"):  # Ctrl+N
            if self.buffer.modified:
                self.set_message(
                    "Unsaved changes! Save first", self.theme.colors.warning
                )
            else:
                self.buffer = TextBuffer()
                self.set_message("New file", self.theme.colors.info)
            return True

        # Open file browser (Ctrl+O)
        if key == ord("\x0f"):  # Ctrl+O
            self.show_browser = not self.show_browser
            if self.show_browser:
                self.browser_focused = True
                self.browser.refresh_files()
                self.set_message("File browser opened", self.theme.colors.info)
            else:
                self.browser_focused = False
                self.set_message("File browser closed", self.theme.colors.info)
            return True

        # Switch focus (TAB)
        if key == ord("\t"):
            if self.show_browser:
                self.browser_focused = not self.browser_focused
                focus_name = "browser" if self.browser_focused else "editor"
                self.set_message(f"Focus: {focus_name}", self.theme.colors.info)
            return True

        # Close browser or clear selection (ESC)
        if key == 27:  # ESC
            if self.show_browser and self.browser_focused:
                self.show_browser = False
                self.browser_focused = False
                self.set_message("Browser closed", self.theme.colors.info)
            else:
                self.message = ""
            return True

        # File browser controls
        if self.browser_focused and self.show_browser:
            if key == curses.KEY_UP:
                self.browser.move_selection(-1)
            elif key == curses.KEY_DOWN:
                self.browser.move_selection(1)
            elif key == curses.KEY_ENTER or key == ord("\n"):
                selected_file = self.browser.enter_selected()
                if selected_file:
                    success, msg = self.buffer.load_file(selected_file)
                    color = (
                        self.theme.colors.success
                        if success
                        else self.theme.colors.error
                    )
                    self.set_message(msg, color)
                    self.show_browser = False
                    self.browser_focused = False
                    self.scroll_row = 0
            return True

        # Editor controls (when editor is focused)
        if not self.browser_focused:
            # Navigation
            if key == curses.KEY_UP:
                self.buffer.move_cursor(-1, 0)
            elif key == curses.KEY_DOWN:
                self.buffer.move_cursor(1, 0)
            elif key == curses.KEY_LEFT:
                self.buffer.move_cursor(0, -1)
            elif key == curses.KEY_RIGHT:
                self.buffer.move_cursor(0, 1)
            elif key == curses.KEY_HOME:
                self.buffer.cursor_col = 0
            elif key == curses.KEY_END:
                self.buffer.cursor_col = len(self.buffer.lines[self.buffer.cursor_row])
            elif key == curses.KEY_PPAGE:  # Page Up
                height = self.height - 5
                self.buffer.move_cursor(-height, 0)
            elif key == curses.KEY_NPAGE:  # Page Down
                height = self.height - 5
                self.buffer.move_cursor(height, 0)
            # Text editing
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                self.buffer.delete_char()
            elif key == curses.KEY_ENTER or key == ord("\n"):
                self.buffer.insert_newline()
            elif 32 <= key <= 126:  # Printable characters
                self.buffer.insert_char(chr(key))

        return True

    def run(self) -> None:
        """Main editor loop."""
        self.set_message(
            "Welcome! F1-F8: Themes | ^O: Open | ^S: Save | ^Q: Quit",
            self.theme.colors.info,
        )

        while True:
            try:
                self.draw()
                key = self.stdscr.getch()

                if not self.handle_key(key):
                    break

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.set_message(f"Error: {e}", self.theme.colors.error)


def main(stdscr):
    """
    Main entry point for the text editor.

    Args:
        stdscr: Curses window from curses.wrapper()
    """
    # Get filename from command line if provided
    filename = sys.argv[1] if len(sys.argv) > 1 else None

    # Create and run editor
    editor = TextEditor(stdscr, filename)
    editor.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nEditor closed.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
