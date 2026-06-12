#!/usr/bin/env python3
"""
Dialog and Modal System Demonstration for curses-themes

This example showcases a comprehensive modal dialog system inspired by classic
Borland Turbo Vision and dBASE interfaces. It demonstrates various dialog types
with proper 3D effects, shadows, and theme integration.

Features demonstrated:
1. Multiple dialog types (info, warning, error, question, custom)
2. Message boxes with semantic colors and icons
3. Input dialogs with validation and themed text fields
4. Confirmation dialogs with Yes/No/Cancel buttons
5. Progress dialog with animated bar
6. Multi-field form dialog with tab navigation
7. File picker dialog with directory tree navigation
8. 3D raised/sunken effects using draw_box_3d (Borland-style)
9. Drop shadow effects for layered dialogs
10. Keyboard shortcuts and focus management
11. Button states (normal, focused, disabled) with theme colors

Controls:
  1 - Show Info Message Box
  2 - Show Warning Message Box
  3 - Show Error Message Box
  4 - Show Question Dialog (Yes/No)
  5 - Show Input Dialog
  6 - Show Multi-field Form
  7 - Show Progress Dialog
  8 - Show File Picker Dialog
  9 - Show Confirmation Dialog (Yes/No/Cancel)
  t - Switch Theme
  q - Quit

In dialogs:
  Tab/Shift+Tab - Navigate between buttons/fields
  Enter/Space - Activate button
  Esc - Cancel/Close
  Arrow Keys - Navigate lists

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Usage:
    python3 dialog_system_demo.py

Requirements:
    - Python 3.6+
    - curses-themes library
    - Terminal with color support
"""

import curses
import time
from typing import List, Tuple, Optional
from curses_themes import ThemeManager


# ============================================================================
# Dialog Base Class and Helper Functions
# ============================================================================


class DialogResult:
    """Represents the result of a dialog interaction."""

    OK = 1
    CANCEL = 2
    YES = 3
    NO = 4
    CLOSE = 5


def draw_centered_text(window, y, x, width, text, color_pair):
    """Draw text centered within a given width."""
    text_x = x + (width - len(text)) // 2
    try:
        window.addstr(y, text_x, text[:width], curses.color_pair(color_pair))
    except curses.error:
        pass


def draw_button(window, theme, y, x, text, focused=False, enabled=True):
    """
    Draw a 3D button with proper state representation.

    Args:
        window: Curses window to draw on
        theme: Active theme
        y: Y coordinate
        x: X coordinate
        text: Button text
        focused: Whether button has focus
        enabled: Whether button is enabled
    """
    width = len(text) + 4
    height = 3

    # Determine color based on state
    if not enabled:
        color = theme.components.disabled
    elif focused:
        color = theme.components.button_focused
    else:
        color = theme.components.button

    # Draw 3D box if theme supports it
    if hasattr(theme, "draw_box_3d"):
        theme.draw_box_3d(window, y, x, height, width, raised=True)
    else:
        # Fallback to regular box
        theme.draw_box(window, y, x, height, width)

    # Draw button text
    attrs = curses.color_pair(color)
    if focused:
        attrs |= curses.A_BOLD
    if not enabled:
        attrs |= curses.A_DIM

    try:
        window.addstr(y + 1, x + 2, text, attrs)
    except curses.error:
        pass


def draw_input_field(window, theme, y, x, width, value="", focused=False):
    """
    Draw a sunken text input field.

    Args:
        window: Curses window to draw on
        theme: Active theme
        y: Y coordinate
        x: X coordinate
        width: Field width
        value: Current value
        focused: Whether field has focus
    """
    # Draw sunken box if theme supports 3D
    if hasattr(theme, "draw_box_3d"):
        theme.draw_box_3d(window, y, x, 3, width, raised=False)
    else:
        theme.draw_box(window, y, x, 3, width)

    # Draw value with cursor if focused
    color = theme.components.text_input
    display_value = value[: width - 4]

    try:
        window.addstr(y + 1, x + 2, display_value, curses.color_pair(color))
        if focused:
            # Show cursor at end of text
            cursor_x = x + 2 + len(display_value)
            if cursor_x < x + width - 2:
                window.addch(
                    y + 1, cursor_x, "_", curses.color_pair(color) | curses.A_BLINK
                )
    except curses.error:
        pass


# ============================================================================
# Message Box Dialogs
# ============================================================================


def show_message_box(stdscr, theme, title, message, dialog_type="info"):
    """
    Show a modal message box with an icon and OK button.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        message: Message text (can be multi-line)
        dialog_type: Type of dialog ("info", "warning", "error", "question")

    Returns:
        DialogResult.OK or DialogResult.CLOSE
    """
    # Determine icon and color based on type
    icons = {
        "info": ("ℹ", theme.colors.info),
        "warning": ("⚠", theme.colors.warning),
        "error": ("✖", theme.colors.error),
        "question": ("?", theme.colors.primary),
    }
    icon, icon_color = icons.get(dialog_type, icons["info"])

    # Calculate dialog dimensions
    lines = message.split("\n")
    msg_width = max(len(line) for line in lines)
    dialog_width = max(msg_width + 8, len(title) + 6, 30)
    dialog_height = len(lines) + 8

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    # Draw dialog box with 3D effect
    if hasattr(theme, "draw_box_3d"):
        theme.draw_box_3d(
            dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
        )
    else:
        theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

    # Draw icon
    try:
        dialog_win.addstr(2, 3, icon, curses.color_pair(icon_color) | curses.A_BOLD)
    except curses.error:
        pass

    # Draw message
    for i, line in enumerate(lines):
        try:
            dialog_win.addstr(
                2 + i,
                6,
                line[: dialog_width - 8],
                curses.color_pair(theme.components.foreground),
            )
        except curses.error:
            pass

    # Draw OK button
    button_y = dialog_height - 4
    button_x = (dialog_width - 8) // 2
    draw_button(dialog_win, theme, button_y, button_x, "OK", focused=True)

    dialog_win.refresh()

    # Wait for key press
    while True:
        key = dialog_win.getch()
        if key in [ord("\n"), ord(" "), 27]:  # Enter, Space, or Esc
            break

    del dialog_win
    stdscr.touchwin()
    stdscr.refresh()

    return DialogResult.OK


# ============================================================================
# Question Dialog (Yes/No)
# ============================================================================


def show_question_dialog(stdscr, theme, title, question):
    """
    Show a Yes/No question dialog.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        question: Question text

    Returns:
        DialogResult.YES or DialogResult.NO
    """
    # Calculate dialog dimensions
    dialog_width = max(len(question) + 8, len(title) + 6, 40)
    dialog_height = 10

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    focused_button = 0  # 0 = Yes, 1 = No

    while True:
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw question icon
        try:
            dialog_win.addstr(
                2, 3, "?", curses.color_pair(theme.colors.primary) | curses.A_BOLD
            )
        except curses.error:
            pass

        # Draw question text
        try:
            dialog_win.addstr(
                2,
                6,
                question[: dialog_width - 8],
                curses.color_pair(theme.components.foreground),
            )
        except curses.error:
            pass

        # Draw Yes and No buttons
        button_y = dialog_height - 4
        yes_x = dialog_width // 2 - 12
        no_x = dialog_width // 2 + 2

        draw_button(
            dialog_win, theme, button_y, yes_x, "Yes", focused=(focused_button == 0)
        )
        draw_button(
            dialog_win, theme, button_y, no_x, "No", focused=(focused_button == 1)
        )

        dialog_win.refresh()

        # Handle key press
        key = dialog_win.getch()

        if key == ord("\t"):  # Tab
            focused_button = 1 - focused_button
        elif key == curses.KEY_LEFT:
            focused_button = 0
        elif key == curses.KEY_RIGHT:
            focused_button = 1
        elif key in [ord("\n"), ord(" ")]:  # Enter or Space
            del dialog_win
            stdscr.touchwin()
            stdscr.refresh()
            return DialogResult.YES if focused_button == 0 else DialogResult.NO
        elif key == 27:  # Esc
            del dialog_win
            stdscr.touchwin()
            stdscr.refresh()
            return DialogResult.NO


# ============================================================================
# Confirmation Dialog (Yes/No/Cancel)
# ============================================================================


def show_confirmation_dialog(stdscr, theme, title, message):
    """
    Show a Yes/No/Cancel confirmation dialog.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        message: Message text

    Returns:
        DialogResult.YES, DialogResult.NO, or DialogResult.CANCEL
    """
    # Calculate dialog dimensions
    dialog_width = max(len(message) + 8, len(title) + 6, 50)
    dialog_height = 10

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    focused_button = 0  # 0 = Yes, 1 = No, 2 = Cancel

    while True:
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw warning icon
        try:
            dialog_win.addstr(
                2, 3, "⚠", curses.color_pair(theme.colors.warning) | curses.A_BOLD
            )
        except curses.error:
            pass

        # Draw message
        try:
            dialog_win.addstr(
                2,
                6,
                message[: dialog_width - 8],
                curses.color_pair(theme.components.foreground),
            )
        except curses.error:
            pass

        # Draw Yes, No, and Cancel buttons
        button_y = dialog_height - 4
        yes_x = dialog_width // 2 - 20
        no_x = dialog_width // 2 - 5
        cancel_x = dialog_width // 2 + 10

        draw_button(
            dialog_win, theme, button_y, yes_x, "Yes", focused=(focused_button == 0)
        )
        draw_button(
            dialog_win, theme, button_y, no_x, "No", focused=(focused_button == 1)
        )
        draw_button(
            dialog_win,
            theme,
            button_y,
            cancel_x,
            "Cancel",
            focused=(focused_button == 2),
        )

        dialog_win.refresh()

        # Handle key press
        key = dialog_win.getch()

        if key == ord("\t"):  # Tab
            focused_button = (focused_button + 1) % 3
        elif key == curses.KEY_BTAB:  # Shift+Tab
            focused_button = (focused_button - 1) % 3
        elif key == curses.KEY_LEFT:
            focused_button = (focused_button - 1) % 3
        elif key == curses.KEY_RIGHT:
            focused_button = (focused_button + 1) % 3
        elif key in [ord("\n"), ord(" ")]:  # Enter or Space
            del dialog_win
            stdscr.touchwin()
            stdscr.refresh()
            if focused_button == 0:
                return DialogResult.YES
            elif focused_button == 1:
                return DialogResult.NO
            else:
                return DialogResult.CANCEL
        elif key == 27:  # Esc
            del dialog_win
            stdscr.touchwin()
            stdscr.refresh()
            return DialogResult.CANCEL


# ============================================================================
# Input Dialog
# ============================================================================


def show_input_dialog(stdscr, theme, title, prompt, default_value=""):
    """
    Show an input dialog with a text field.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        prompt: Input prompt
        default_value: Default input value

    Returns:
        Tuple of (DialogResult, value) or (DialogResult.CANCEL, None)
    """
    # Calculate dialog dimensions
    dialog_width = max(len(prompt) + 8, len(title) + 6, 50)
    dialog_height = 12

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    input_value = default_value
    focused_item = 0  # 0 = input field, 1 = OK, 2 = Cancel

    while True:
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw prompt
        try:
            dialog_win.addstr(
                2, 3, prompt, curses.color_pair(theme.components.foreground)
            )
        except curses.error:
            pass

        # Draw input field
        field_width = dialog_width - 6
        draw_input_field(
            dialog_win,
            theme,
            4,
            3,
            field_width,
            input_value,
            focused=(focused_item == 0),
        )

        # Draw OK and Cancel buttons
        button_y = dialog_height - 4
        ok_x = dialog_width // 2 - 12
        cancel_x = dialog_width // 2 + 2

        draw_button(
            dialog_win, theme, button_y, ok_x, "OK", focused=(focused_item == 1)
        )
        draw_button(
            dialog_win, theme, button_y, cancel_x, "Cancel", focused=(focused_item == 2)
        )

        dialog_win.refresh()

        # Handle key press
        key = dialog_win.getch()

        if focused_item == 0:  # Input field has focus
            if key == ord("\t"):  # Tab
                focused_item = 1
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                input_value = input_value[:-1]
            elif key == ord("\n"):
                focused_item = 1
            elif 32 <= key <= 126:
                input_value += chr(key)
        else:  # Button has focus
            if key == ord("\t"):  # Tab
                focused_item = 2 if focused_item == 1 else 1
            elif key == curses.KEY_BTAB:  # Shift+Tab
                if focused_item == 1:
                    focused_item = 0
                else:
                    focused_item = 1
            elif key == curses.KEY_LEFT:
                focused_item = 1 if focused_item == 2 else 0
            elif key == curses.KEY_RIGHT:
                focused_item = 2 if focused_item == 1 else 0
            elif key in [ord("\n"), ord(" ")]:  # Enter or Space
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                if focused_item == 1:
                    return (DialogResult.OK, input_value)
                else:
                    return (DialogResult.CANCEL, None)
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)


# ============================================================================
# Multi-field Form Dialog
# ============================================================================


def show_form_dialog(stdscr, theme, title, fields):
    """
    Show a multi-field form dialog with tab navigation.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        fields: List of (label, default_value) tuples

    Returns:
        Tuple of (DialogResult, values_dict) or (DialogResult.CANCEL, None)
    """
    # Calculate dialog dimensions
    max_label_len = max(len(label) for label, _ in fields)
    dialog_width = max(max_label_len + 35, len(title) + 6, 50)
    dialog_height = len(fields) * 4 + 8

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    # Initialize field values
    field_values = [default for _, default in fields]
    num_fields = len(fields)
    focused_item = (
        0  # 0 to num_fields-1 = fields, num_fields = OK, num_fields+1 = Cancel
    )

    while True:
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw fields
        for i, (label, _) in enumerate(fields):
            field_y = 2 + i * 4

            # Draw label
            try:
                dialog_win.addstr(
                    field_y,
                    3,
                    label + ":",
                    curses.color_pair(theme.components.foreground),
                )
            except curses.error:
                pass

            # Draw input field
            field_width = dialog_width - max_label_len - 8
            draw_input_field(
                dialog_win,
                theme,
                field_y + 1,
                max_label_len + 5,
                field_width,
                field_values[i],
                focused=(focused_item == i),
            )

        # Draw OK and Cancel buttons
        button_y = dialog_height - 4
        ok_x = dialog_width // 2 - 12
        cancel_x = dialog_width // 2 + 2

        draw_button(
            dialog_win,
            theme,
            button_y,
            ok_x,
            "OK",
            focused=(focused_item == num_fields),
        )
        draw_button(
            dialog_win,
            theme,
            button_y,
            cancel_x,
            "Cancel",
            focused=(focused_item == num_fields + 1),
        )

        dialog_win.refresh()

        # Handle key press
        key = dialog_win.getch()

        if focused_item < num_fields:  # A field has focus
            if key == ord("\t"):  # Tab
                focused_item = (focused_item + 1) % (num_fields + 2)
            elif key == curses.KEY_BTAB:  # Shift+Tab
                focused_item = (focused_item - 1) % (num_fields + 2)
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                field_values[focused_item] = field_values[focused_item][:-1]
            elif key == ord("\n"):
                focused_item = (focused_item + 1) % (num_fields + 2)
            elif 32 <= key <= 126:
                field_values[focused_item] += chr(key)
        else:  # Button has focus
            if key == ord("\t"):  # Tab
                focused_item = (focused_item + 1) % (num_fields + 2)
            elif key == curses.KEY_BTAB:  # Shift+Tab
                focused_item = (focused_item - 1) % (num_fields + 2)
            elif key == curses.KEY_LEFT:
                focused_item = (
                    num_fields if focused_item == num_fields + 1 else num_fields + 1
                )
            elif key == curses.KEY_RIGHT:
                focused_item = (
                    num_fields + 1 if focused_item == num_fields else num_fields
                )
            elif key in [ord("\n"), ord(" ")]:  # Enter or Space
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                if focused_item == num_fields:
                    # Return values as dictionary
                    result = {
                        label: value for (label, _), value in zip(fields, field_values)
                    }
                    return (DialogResult.OK, result)
                else:
                    return (DialogResult.CANCEL, None)
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)


# ============================================================================
# Progress Dialog
# ============================================================================


def show_progress_dialog(stdscr, theme, title, message):
    """
    Show a progress dialog with animated progress bar.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title
        message: Progress message
    """
    # Calculate dialog dimensions
    dialog_width = max(len(message) + 8, len(title) + 6, 50)
    dialog_height = 10

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    # Animate progress bar
    for progress in range(0, 101, 5):
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw message
        try:
            dialog_win.addstr(
                2, 3, message, curses.color_pair(theme.components.foreground)
            )
        except curses.error:
            pass

        # Draw progress bar border (sunken)
        bar_width = dialog_width - 6
        bar_y = 4
        bar_x = 3

        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(dialog_win, bar_y, bar_x, 3, bar_width, raised=False)
        else:
            theme.draw_box(dialog_win, bar_y, bar_x, 3, bar_width)

        # Draw progress bar fill
        fill_width = int((bar_width - 4) * progress / 100)
        try:
            for i in range(fill_width):
                dialog_win.addch(
                    bar_y + 1,
                    bar_x + 2 + i,
                    "█",
                    curses.color_pair(theme.colors.primary),
                )
        except curses.error:
            pass

        # Draw percentage
        percent_text = f"{progress}%"
        try:
            dialog_win.addstr(
                bar_y + 1,
                bar_x + bar_width - len(percent_text) - 2,
                percent_text,
                curses.color_pair(theme.components.foreground) | curses.A_BOLD,
            )
        except curses.error:
            pass

        dialog_win.refresh()

        # Small delay to show animation
        curses.napms(50)

        # Check for Esc key to cancel
        dialog_win.nodelay(True)
        key = dialog_win.getch()
        dialog_win.nodelay(False)
        if key == 27:
            break

    # Show completion
    time.sleep(0.5)

    del dialog_win
    stdscr.touchwin()
    stdscr.refresh()


# ============================================================================
# File Picker Dialog
# ============================================================================


def show_file_picker_dialog(stdscr, theme, title):
    """
    Show a file picker dialog with directory navigation.

    Args:
        stdscr: Main curses window
        theme: Active theme
        title: Dialog title

    Returns:
        Tuple of (DialogResult, selected_file) or (DialogResult.CANCEL, None)
    """
    import os

    # Calculate dialog dimensions
    dialog_width = 60
    dialog_height = 20

    # Calculate centered position
    screen_h, screen_w = stdscr.getmaxyx()
    dialog_y = (screen_h - dialog_height) // 2
    dialog_x = (screen_w - dialog_width) // 2

    # Create dialog window
    dialog_win = curses.newwin(dialog_height, dialog_width, dialog_y, dialog_x)

    # Get list of files in current directory
    try:
        current_dir = os.getcwd()
        items = [".."] + sorted(os.listdir(current_dir))
    except:
        items = [".."]

    selected_index = 0
    scroll_offset = 0
    max_visible = dialog_height - 8
    focused_item = 0  # 0 = list, 1 = OK, 2 = Cancel

    while True:
        dialog_win.clear()

        # Draw dialog box
        if hasattr(theme, "draw_box_3d"):
            theme.draw_box_3d(
                dialog_win, 0, 0, dialog_height, dialog_width, raised=True, title=title
            )
        else:
            theme.draw_box(dialog_win, 0, 0, dialog_height, dialog_width, title=title)

        # Draw current directory
        try:
            dir_text = f"Directory: {os.path.basename(current_dir) or current_dir}"
            dialog_win.addstr(
                2,
                3,
                dir_text[: dialog_width - 6],
                curses.color_pair(theme.components.foreground),
            )
        except curses.error:
            pass

        # Draw file list
        list_y = 4
        for i in range(max_visible):
            item_index = scroll_offset + i
            if item_index >= len(items):
                break

            item = items[item_index]
            is_selected = item_index == selected_index and focused_item == 0

            # Determine if item is a directory
            try:
                full_path = os.path.join(current_dir, item)
                is_dir = os.path.isdir(full_path) or item == ".."
                prefix = "[DIR] " if is_dir else "      "
            except:
                prefix = "      "

            display_text = prefix + item

            if is_selected:
                color = theme.components.selection
                attrs = curses.color_pair(color) | curses.A_REVERSE
            else:
                color = theme.components.foreground
                attrs = curses.color_pair(color)

            try:
                dialog_win.addstr(
                    list_y + i, 3, display_text[: dialog_width - 6], attrs
                )
            except curses.error:
                pass

        # Draw OK and Cancel buttons
        button_y = dialog_height - 4
        ok_x = dialog_width // 2 - 12
        cancel_x = dialog_width // 2 + 2

        draw_button(
            dialog_win, theme, button_y, ok_x, "OK", focused=(focused_item == 1)
        )
        draw_button(
            dialog_win, theme, button_y, cancel_x, "Cancel", focused=(focused_item == 2)
        )

        dialog_win.refresh()

        # Handle key press
        key = dialog_win.getch()

        if focused_item == 0:  # List has focus
            if key == curses.KEY_UP:
                if selected_index > 0:
                    selected_index -= 1
                    if selected_index < scroll_offset:
                        scroll_offset = selected_index
            elif key == curses.KEY_DOWN:
                if selected_index < len(items) - 1:
                    selected_index += 1
                    if selected_index >= scroll_offset + max_visible:
                        scroll_offset = selected_index - max_visible + 1
            elif key == ord("\t"):  # Tab
                focused_item = 1
            elif key in [ord("\n"), ord(" ")]:  # Enter
                # Navigate to directory or select file
                selected_item = items[selected_index]
                try:
                    if selected_item == "..":
                        current_dir = os.path.dirname(current_dir)
                    else:
                        full_path = os.path.join(current_dir, selected_item)
                        if os.path.isdir(full_path):
                            current_dir = full_path
                        else:
                            # File selected
                            del dialog_win
                            stdscr.touchwin()
                            stdscr.refresh()
                            return (DialogResult.OK, full_path)

                    # Update file list
                    items = [".."] + sorted(os.listdir(current_dir))
                    selected_index = 0
                    scroll_offset = 0
                except:
                    pass
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)
        else:  # Button has focus
            if key == ord("\t"):  # Tab
                focused_item = 2 if focused_item == 1 else 1
            elif key == curses.KEY_BTAB:  # Shift+Tab
                if focused_item == 1:
                    focused_item = 0
                else:
                    focused_item = 1
            elif key == curses.KEY_LEFT:
                focused_item = 1 if focused_item == 2 else 0
            elif key == curses.KEY_RIGHT:
                focused_item = 2 if focused_item == 1 else 0
            elif key in [ord("\n"), ord(" ")]:  # Enter or Space
                if focused_item == 1:
                    # OK - return selected file
                    selected_item = items[selected_index]
                    try:
                        full_path = os.path.join(current_dir, selected_item)
                        if not os.path.isdir(full_path):
                            del dialog_win
                            stdscr.touchwin()
                            stdscr.refresh()
                            return (DialogResult.OK, full_path)
                    except:
                        pass
                else:
                    # Cancel
                    del dialog_win
                    stdscr.touchwin()
                    stdscr.refresh()
                    return (DialogResult.CANCEL, None)
            elif key == 27:  # Esc
                del dialog_win
                stdscr.touchwin()
                stdscr.refresh()
                return (DialogResult.CANCEL, None)


# ============================================================================
# Main Demo Screen
# ============================================================================


def draw_main_screen(stdscr, theme, last_result=""):
    """Draw the main demo screen with menu options."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Title
    title = "Dialog and Modal System Demo"
    try:
        stdscr.addstr(
            1,
            (width - len(title)) // 2,
            title,
            curses.color_pair(theme.colors.primary) | curses.A_BOLD,
        )
    except curses.error:
        pass

    # Theme name
    theme_text = f"Theme: {theme.name}"
    try:
        stdscr.addstr(
            2,
            (width - len(theme_text)) // 2,
            theme_text,
            curses.color_pair(theme.components.foreground),
        )
    except curses.error:
        pass

    # Menu options
    menu_items = [
        "",
        "Dialog Types:",
        "",
        "  [1] Info Message Box",
        "  [2] Warning Message Box",
        "  [3] Error Message Box",
        "  [4] Question Dialog (Yes/No)",
        "  [5] Input Dialog",
        "  [6] Multi-field Form Dialog",
        "  [7] Progress Dialog",
        "  [8] File Picker Dialog",
        "  [9] Confirmation Dialog (Yes/No/Cancel)",
        "",
        "Controls:",
        "",
        "  [t] Switch Theme",
        "  [q] Quit",
    ]

    start_y = 4
    for i, item in enumerate(menu_items):
        try:
            if item.startswith("  ["):
                # Highlight menu items
                stdscr.addstr(
                    start_y + i, 5, item, curses.color_pair(theme.components.button)
                )
            elif item.endswith(":"):
                # Section headers
                stdscr.addstr(
                    start_y + i,
                    5,
                    item,
                    curses.color_pair(theme.colors.accent) | curses.A_BOLD,
                )
            else:
                stdscr.addstr(
                    start_y + i, 5, item, curses.color_pair(theme.components.foreground)
                )
        except curses.error:
            pass

    # Last result
    if last_result:
        result_y = height - 3
        try:
            stdscr.addstr(
                result_y,
                5,
                "Last Result: " + last_result,
                curses.color_pair(theme.colors.info),
            )
        except curses.error:
            pass

    stdscr.refresh()


# ============================================================================
# Main Loop
# ============================================================================


def main(stdscr):
    """Main demo loop."""
    # Initialize curses
    curses.curs_set(0)  # Hide cursor

    # Available themes
    theme_names = ["borland-3d", "dbase-iv-3d", "dos", "dbase-iii", "dark", "light"]
    current_theme_idx = 0

    # Try to load first available theme
    theme = None
    for i, name in enumerate(theme_names):
        try:
            theme = ThemeManager.load(name)
            theme.apply(stdscr)
            current_theme_idx = i
            break
        except:
            continue

    # Fallback to default if no theme loaded
    if theme is None:
        theme = ThemeManager.load("default")
        theme.apply(stdscr)

    last_result = ""

    while True:
        draw_main_screen(stdscr, theme, last_result)

        # Wait for key press
        key = stdscr.getch()

        if key == ord("q") or key == ord("Q"):
            break
        elif key == ord("t") or key == ord("T"):
            # Switch theme
            current_theme_idx = (current_theme_idx + 1) % len(theme_names)
            try:
                theme = ThemeManager.load(theme_names[current_theme_idx])
                theme.apply(stdscr)
                last_result = f"Switched to {theme.name}"
            except Exception as e:
                last_result = f"Error loading theme: {str(e)}"
        elif key == ord("1"):
            # Info message box
            show_message_box(
                stdscr,
                theme,
                "Information",
                "This is an informational message.\nIt can span multiple lines.",
                "info",
            )
            last_result = "Info dialog closed"
        elif key == ord("2"):
            # Warning message box
            show_message_box(
                stdscr,
                theme,
                "Warning",
                "This is a warning message.\nPlease be careful!",
                "warning",
            )
            last_result = "Warning dialog closed"
        elif key == ord("3"):
            # Error message box
            show_message_box(
                stdscr,
                theme,
                "Error",
                "An error has occurred!\nPlease check your input.",
                "error",
            )
            last_result = "Error dialog closed"
        elif key == ord("4"):
            # Question dialog
            result = show_question_dialog(
                stdscr, theme, "Confirm Action", "Do you want to proceed?"
            )
            last_result = (
                f"Question result: {'Yes' if result == DialogResult.YES else 'No'}"
            )
        elif key == ord("5"):
            # Input dialog
            result, value = show_input_dialog(
                stdscr, theme, "Enter Name", "Please enter your name:", "John Doe"
            )
            if result == DialogResult.OK:
                last_result = f"Input value: {value}"
            else:
                last_result = "Input cancelled"
        elif key == ord("6"):
            # Multi-field form
            fields = [
                ("Name", "John Doe"),
                ("Email", "john@example.com"),
                ("Phone", "+1-555-0123"),
                ("Company", "Acme Corp"),
            ]
            result, values = show_form_dialog(
                stdscr, theme, "Registration Form", fields
            )
            if result == DialogResult.OK:
                last_result = f"Form submitted: {len(values)} fields"
            else:
                last_result = "Form cancelled"
        elif key == ord("7"):
            # Progress dialog
            show_progress_dialog(
                stdscr, theme, "Processing", "Please wait while processing..."
            )
            last_result = "Progress completed"
        elif key == ord("8"):
            # File picker
            result, filepath = show_file_picker_dialog(stdscr, theme, "Select File")
            if result == DialogResult.OK:
                import os

                last_result = f"Selected: {os.path.basename(filepath)}"
            else:
                last_result = "File selection cancelled"
        elif key == ord("9"):
            # Confirmation dialog
            result = show_confirmation_dialog(
                stdscr, theme, "Confirm", "Save changes before closing?"
            )
            if result == DialogResult.YES:
                last_result = "Confirmation: Yes"
            elif result == DialogResult.NO:
                last_result = "Confirmation: No"
            else:
                last_result = "Confirmation: Cancel"


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
