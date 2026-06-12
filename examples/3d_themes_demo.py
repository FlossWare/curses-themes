#!/usr/bin/env python3
"""
Interactive 3D Themes Demonstration

Showcases Borland-style 3D effects with raised windows, drop shadows,
sunken input fields, and theme switching.

This demo demonstrates:
1. Borland3DTheme with raised windows and drop shadows
2. DBase4_3DTheme with Control Center style 3D effects
3. Side-by-side comparison of both themes
4. Raised buttons vs sunken input fields
5. Multiple overlapping windows showing shadow effects
6. Interactive theme switching

Controls:
  n - Next theme
  b - Switch to Borland3DTheme
  d - Switch to DBase4_3DTheme
  q - Quit

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
"""

import curses

from curses_themes import ThemeManager


def draw_shadow(window, y, x, height, width, color_pair):
    """
    Draw a drop shadow effect for a window.

    Args:
        window: Curses window to draw on
        y: Top-left Y coordinate of the shadow
        x: Top-left X coordinate of the shadow
        height: Shadow height
        width: Shadow width
        color_pair: Color pair for the shadow
    """
    max_y, max_x = window.getmaxyx()

    # Draw right shadow (vertical)
    for i in range(1, height):
        if y + i < max_y and x + width < max_x:
            try:
                window.addch(y + i, x + width, " ", curses.color_pair(color_pair))
                if x + width + 1 < max_x:
                    window.addch(
                        y + i, x + width + 1, " ", curses.color_pair(color_pair)
                    )
            except curses.error:
                pass

    # Draw bottom shadow (horizontal)
    for i in range(width + 2):
        if y + height < max_y and x + i < max_x:
            try:
                window.addch(y + height, x + i, " ", curses.color_pair(color_pair))
            except curses.error:
                pass


def draw_3d_box(window, theme, y, x, height, width, title="", raised=True):
    """
    Draw a 3D box with shadow effects.

    Args:
        window: Curses window to draw on
        theme: Theme object with draw_box_3d method or fallback to draw_box
        y: Top-left Y coordinate
        x: Top-left X coordinate
        height: Box height
        width: Box width
        title: Optional title for the box
        raised: True for raised (button-like), False for sunken (input-like)
    """
    # Use draw_box_3d if available, otherwise use draw_box
    if hasattr(theme, "draw_box_3d"):
        theme.draw_box_3d(window, y, x, height, width, title=title, raised=raised)
    else:
        # Fallback: simulate 3D with regular box and shadow
        theme.draw_box(window, y, x, height, width, title=title)

        # Add shadow for raised boxes
        if raised:
            try:
                # Try to get a darker color for shadow (disabled or background)
                shadow_color = theme.components.disabled
                draw_shadow(window, y, x, height, width, shadow_color)
            except (AttributeError, curses.error):
                # Ignore if shadow color not available or drawing fails at boundaries
                pass


def draw_raised_button(window, theme, y, x, text, focused=False):
    """
    Draw a raised 3D button.

    Args:
        window: Curses window to draw on
        theme: Theme object
        y: Y coordinate
        x: X coordinate
        text: Button text
        focused: Whether the button is focused
    """
    width = len(text) + 4
    height = 3

    # Draw 3D box
    draw_3d_box(window, theme, y, x, height, width, raised=True)

    # Draw button text
    color = theme.components.button_focused if focused else theme.components.button
    try:
        window.addstr(
            y + 1,
            x + 2,
            text,
            curses.color_pair(color) | (curses.A_BOLD if focused else 0),
        )
    except curses.error:
        pass


def draw_sunken_input(window, theme, y, x, width, label="", value=""):
    """
    Draw a sunken 3D input field.

    Args:
        window: Curses window to draw on
        theme: Theme object
        y: Y coordinate
        x: X coordinate
        width: Input field width
        label: Optional label for the input
        value: Current input value
    """
    # Draw label if provided
    if label:
        try:
            window.addstr(y, x, label, curses.color_pair(theme.colors.foreground))
            y += 1
        except curses.error:
            pass

    # Draw sunken box for input
    draw_3d_box(window, theme, y, x, 3, width, raised=False)

    # Draw input value
    try:
        window.addstr(
            y + 1,
            x + 2,
            value[: width - 4],
            curses.color_pair(theme.components.text_input),
        )
    except curses.error:
        pass


def draw_overlapping_windows(stdscr, theme):
    """
    Draw multiple overlapping windows to demonstrate shadow effects.

    Args:
        stdscr: Main curses window
        theme: Current theme
    """
    height, width = stdscr.getmaxyx()

    # Back window
    if height > 20 and width > 70:
        draw_3d_box(stdscr, theme, 8, 10, 12, 35, title="Back Window", raised=True)
        try:
            stdscr.addstr(
                10,
                13,
                "This window is behind",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                11,
                13,
                "the front window.",
                curses.color_pair(theme.colors.foreground),
            )
        except curses.error:
            pass

    # Middle window
    if height > 18 and width > 65:
        draw_3d_box(stdscr, theme, 6, 20, 12, 35, title="Middle Window", raised=True)
        try:
            stdscr.addstr(
                8,
                23,
                "Notice the drop shadow",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                9,
                23,
                "effects as windows",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                10,
                23,
                "overlap each other.",
                curses.color_pair(theme.colors.foreground),
            )
        except curses.error:
            pass

    # Front window
    if height > 16 and width > 60:
        draw_3d_box(stdscr, theme, 4, 30, 12, 35, title="Front Window", raised=True)
        try:
            stdscr.addstr(
                6,
                33,
                "Multiple overlapping",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                7,
                33,
                "windows demonstrate",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                8,
                33,
                "the 3D shadow effects",
                curses.color_pair(theme.colors.foreground),
            )
            stdscr.addstr(
                9,
                33,
                "of Borland-style UIs.",
                curses.color_pair(theme.colors.foreground),
            )
        except curses.error:
            pass


def draw_demo_screen(stdscr, theme):
    """
    Draw the complete demo screen with all 3D effects.

    Args:
        stdscr: Main curses window
        theme: Current theme
    """
    height, width = stdscr.getmaxyx()

    # Clear screen
    stdscr.clear()

    # Title bar
    title = f"3D Theme Demo: {theme.name}"
    try:
        stdscr.addstr(
            0,
            (width - len(title)) // 2,
            title,
            curses.color_pair(theme.components.button_focused) | curses.A_BOLD,
        )
    except curses.error:
        pass

    # Description
    if hasattr(theme, "description") and theme.description:
        desc = theme.description.split("\n")[0][: width - 4]
        try:
            stdscr.addstr(1, 2, desc, curses.color_pair(theme.colors.foreground))
        except curses.error:
            pass

    # Left panel: Raised elements
    panel_y = 3
    try:
        stdscr.addstr(
            panel_y,
            2,
            "RAISED ELEMENTS:",
            curses.color_pair(theme.components.selection) | curses.A_BOLD,
        )
    except curses.error:
        pass

    # Draw raised buttons
    draw_raised_button(stdscr, theme, panel_y + 2, 2, "Normal Button", focused=False)
    draw_raised_button(stdscr, theme, panel_y + 6, 2, "Focused Button", focused=True)
    draw_raised_button(stdscr, theme, panel_y + 10, 2, "OK", focused=False)
    draw_raised_button(stdscr, theme, panel_y + 10, 15, "Cancel", focused=False)

    # Right panel: Sunken elements (if screen is wide enough)
    if width > 50:
        try:
            stdscr.addstr(
                panel_y,
                30,
                "SUNKEN ELEMENTS:",
                curses.color_pair(theme.components.selection) | curses.A_BOLD,
            )
        except curses.error:
            pass

        # Draw sunken input fields
        draw_sunken_input(
            stdscr, theme, panel_y + 2, 30, 25, label="Name:", value="John Doe"
        )
        draw_sunken_input(
            stdscr, theme, panel_y + 6, 30, 25, label="Email:", value="john@example.com"
        )
        draw_sunken_input(
            stdscr, theme, panel_y + 10, 30, 25, label="Password:", value="********"
        )

    # Bottom section: Overlapping windows demo
    if height > 25:
        try:
            stdscr.addstr(
                20,
                2,
                "OVERLAPPING WINDOWS WITH SHADOWS:",
                curses.color_pair(theme.components.selection) | curses.A_BOLD,
            )
        except curses.error:
            pass
        draw_overlapping_windows(stdscr, theme)

    # Instructions at bottom
    instructions = [
        "Controls: [n]ext theme  [b]orland  [d]BASE-IV  [q]uit",
    ]

    for i, instruction in enumerate(instructions):
        try:
            y = height - len(instructions) + i - 1
            stdscr.addstr(
                y,
                (width - len(instruction)) // 2,
                instruction,
                curses.color_pair(theme.components.button) | curses.A_BOLD,
            )
        except curses.error:
            pass

    stdscr.refresh()


def main(stdscr):
    """
    Main demo loop with theme switching.

    Args:
        stdscr: Main curses window
    """
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor

    # Theme names for cycling
    theme_names = ["borland-3d", "dbase-iv-3d"]

    # Try to load 3D themes, fall back to regular themes if not available
    available_themes = []
    for name in theme_names:
        try:
            # Try loading the 3D theme
            theme = ThemeManager.load(name)
            available_themes.append(name)
        except RuntimeError:
            # Fall back to base theme if 3D version doesn't exist
            base_name = name.replace("-3d", "")
            try:
                theme = ThemeManager.load(base_name)
                available_themes.append(base_name)
            except RuntimeError:
                # Skip this theme if neither version works
                pass
        except Exception:
            # Skip themes that fail to load for other reasons
            pass

    # If no themes available, use default
    if not available_themes:
        available_themes = ["default"]

    current_idx = 0

    while True:
        # Load and apply current theme
        try:
            theme = ThemeManager.load(available_themes[current_idx])
            theme.apply(stdscr)
        except RuntimeError:
            # Fall back to default theme if theme application fails
            try:
                theme = ThemeManager.load("default")
                theme.apply(stdscr)
            except Exception:
                # If even default fails, exit gracefully
                return
        except Exception:
            # Unknown error - try default theme
            try:
                theme = ThemeManager.load("default")
                theme.apply(stdscr)
            except Exception:
                return

        # Draw the demo screen
        draw_demo_screen(stdscr, theme)

        # Wait for keypress
        key = stdscr.getch()

        # Handle key commands
        if key == ord("q") or key == ord("Q"):
            break
        elif key == ord("n") or key == ord("N"):
            # Next theme
            current_idx = (current_idx + 1) % len(available_themes)
        elif key == ord("b") or key == ord("B"):
            # Switch to Borland theme
            for i, name in enumerate(available_themes):
                if "borland" in name.lower():
                    current_idx = i
                    break
        elif key == ord("d") or key == ord("D"):
            # Switch to dBASE-IV theme
            for i, name in enumerate(available_themes):
                if "dbase" in name.lower():
                    current_idx = i
                    break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
