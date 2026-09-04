#!/usr/bin/env python3
"""
Interactive theme switcher demonstration.

This example demonstrates runtime theme switching with the curses-themes library.
Users can cycle through all available themes and see changes applied immediately.

Controls:
    n: Next theme
    p: Previous theme
    q: Quit

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import curses
import os
import sys

# Add parent directory to path to allow running from examples directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from curses_tui import ThemeManager


def draw_theme_demo(
    stdscr, theme, theme_name: str, theme_index: int, total_themes: int
):
    """
    Draw the theme demonstration screen.

    Args:
        stdscr: Curses window object
        theme: Current Theme instance
        theme_name: Name of the current theme
        theme_index: Current theme index (0-based)
        total_themes: Total number of available themes
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Title
    title = "=== Interactive Theme Switcher ==="
    stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

    # Current theme info
    theme_info = f"Theme {theme_index + 1} of {total_themes}: {theme_name}"
    stdscr.addstr(1, (width - len(theme_info)) // 2, theme_info)

    # Instructions
    instructions = "Press 'n' for next, 'p' for previous, 'q' to quit"
    stdscr.addstr(2, (width - len(instructions)) // 2, instructions)

    # Separator
    stdscr.addstr(3, 0, "=" * width)

    # Sample text showing all semantic colors
    y = 5
    x_label = 5
    x_sample = 25

    stdscr.addstr(y, x_label, "Semantic Colors:")
    y += 2

    # Primary - theme.colors.X is a color pair NUMBER - must wrap in curses.color_pair()
    stdscr.addstr(y, x_label, "Primary:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y, x_sample, "Important UI elements", curses.color_pair(theme.colors.primary)
    )
    y += 1

    # Success
    stdscr.addstr(y, x_label, "Success:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y,
        x_sample,
        "Operation completed successfully",
        curses.color_pair(theme.colors.success),
    )
    y += 1

    # Error
    stdscr.addstr(y, x_label, "Error:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y, x_sample, "Critical error occurred", curses.color_pair(theme.colors.error)
    )
    y += 1

    # Warning
    stdscr.addstr(y, x_label, "Warning:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y,
        x_sample,
        "Caution: proceed carefully",
        curses.color_pair(theme.colors.warning),
    )
    y += 1

    # Info
    stdscr.addstr(y, x_label, "Info:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y, x_sample, "Helpful information", curses.color_pair(theme.colors.info)
    )
    y += 1

    # Accent
    stdscr.addstr(y, x_label, "Accent:", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        y, x_sample, "Secondary highlights", curses.color_pair(theme.colors.accent)
    )
    y += 2

    # Sample boxes with different colors
    y += 1
    stdscr.addstr(y, x_label, "Themed Boxes:")
    y += 2

    # Box with border color
    box_width = 30
    box_height = 5
    theme.draw_box(stdscr, y, x_label, box_height, box_width, title="Border Color")
    stdscr.addstr(y + 2, x_label + 2, "Using border color", theme.components.border)

    # Box with primary color
    theme.draw_box(
        stdscr,
        y,
        x_label + box_width + 2,
        box_height,
        box_width,
        title="Primary Color",
        color_pair=theme.colors.primary,
    )
    stdscr.addstr(
        y + 2, x_label + box_width + 4, "Using primary color", theme.colors.primary
    )

    y += box_height + 1

    # Box with success color
    theme.draw_box(
        stdscr,
        y,
        x_label,
        box_height,
        box_width,
        title="Success",
        color_pair=theme.colors.success,
    )
    stdscr.addstr(
        y + 2,
        x_label + 2,
        "Using success color",
        curses.color_pair(theme.colors.success),
    )

    # Box with error color
    theme.draw_box(
        stdscr,
        y,
        x_label + box_width + 2,
        box_height,
        box_width,
        title="Error",
        color_pair=theme.colors.error,
    )
    stdscr.addstr(
        y + 2, x_label + box_width + 4, "Using error color", theme.colors.error
    )

    stdscr.refresh()


def main(stdscr):
    """
    Main application loop for the interactive theme switcher.

    Args:
        stdscr: Curses window object from curses.wrapper()
    """
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable keypad for special keys

    # Get all available themes
    theme_names = ["default", "dark", "light"]
    current_index = 0

    # Load and apply initial theme
    try:
        current_theme = ThemeManager.load(theme_names[current_index])
        current_theme.apply(stdscr)
    except Exception as e:
        # Fall back to default theme on error
        stdscr.addstr(0, 0, f"Error loading theme: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    # Main event loop
    while True:
        # Draw the current theme demonstration
        draw_theme_demo(
            stdscr,
            current_theme,
            theme_names[current_index],
            current_index,
            len(theme_names),
        )

        # Get user input
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        # Handle key presses
        if key == ord("q") or key == ord("Q"):
            # Quit
            break
        elif key == ord("n") or key == ord("N"):
            # Next theme
            current_index = (current_index + 1) % len(theme_names)
            try:
                current_theme = ThemeManager.load(theme_names[current_index])
                current_theme.apply(stdscr)
            except Exception:
                # Fall back to previous working theme on error
                current_index = (current_index - 1) % len(theme_names)
        elif key == ord("p") or key == ord("P"):
            # Previous theme
            current_index = (current_index - 1) % len(theme_names)
            try:
                current_theme = ThemeManager.load(theme_names[current_index])
                current_theme.apply(stdscr)
            except Exception:
                # Fall back to next working theme on error
                current_index = (current_index + 1) % len(theme_names)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nTheme switcher closed.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
