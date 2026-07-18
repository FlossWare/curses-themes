#!/usr/bin/env python3
"""
Example demonstrating how to create a custom theme.

This example shows how to:
- Define a custom theme class (SolarizedDarkTheme)
- Use color_map and component_colors class attributes
- Register the theme with ThemeManager
- Load and apply the custom theme
- Display sample text using theme colors
- Use curses.wrapper() for proper terminal handling

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import curses

from curses_themes import Theme, ThemeManager


class SolarizedDarkTheme(Theme):
    """
    Custom theme based on the Solarized Dark color scheme.

    Solarized is a sixteen color palette designed by Ethan Schoonover
    for use with terminal and GUI applications. It features carefully
    chosen colors that reduce eye strain.

    See: https://ethanschoonover.com/solarized/
    """

    # Solarized base colors
    _base03 = (0, 43, 54)  # Dark background
    _base02 = (7, 54, 66)  # Darker background highlights
    _base0 = (131, 148, 150)  # Primary content

    # Solarized accent colors
    _yellow = (181, 137, 0)
    _red = (220, 50, 47)
    _violet = (108, 113, 196)
    _blue = (38, 139, 210)
    _cyan = (42, 161, 152)
    _green = (133, 153, 0)

    color_map = {
        "background": _base03,  # Dark background
        "foreground": _base0,  # Primary text
        "primary": _blue,  # Main UI highlights
        "success": _green,  # Positive feedback
        "error": _red,  # Error messages
        "warning": _yellow,  # Warnings
        "info": _cyan,  # Information
        "accent": _violet,  # Secondary highlights
    }

    component_colors = {
        "background": (_base0, _base03),
        "button": (_blue, _base02),
        "button_focused": (_base03, _blue),
        "text_input": (_base0, _base02),
        "border": (_cyan, _base03),
        "selection": (_base03, _yellow),
        "disabled": (_base02, _base03),
    }

    def __init__(self):
        """Initialize the Solarized Dark theme."""
        super().__init__(
            name="Solarized Dark",
            description="Professional dark theme with carefully balanced colors",
            author="FlossWare",
        )


def main(stdscr):
    """
    Main application demonstrating the custom theme.

    Args:
        stdscr: The main curses window object.
    """
    # Clear screen and hide cursor
    stdscr.clear()
    curses.curs_set(0)

    # Register the custom theme with ThemeManager
    # Theme lifecycle: 1) Register theme class, 2) Load theme by slug, 3) Apply to window
    ThemeManager.register(SolarizedDarkTheme)

    # Load and apply the custom theme
    try:
        theme = ThemeManager.load("solarized-dark")
        theme.apply(stdscr)
    except RuntimeError as e:
        # Terminal doesn't support colors or theme init failed
        stdscr.addstr(0, 0, f"Theme error: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    # Display theme information
    row = 0
    stdscr.addstr(row, 0, "Custom Theme Example", curses.A_BOLD)
    row += 1
    stdscr.addstr(row, 0, "=" * 60)
    row += 2

    stdscr.addstr(row, 0, f"Theme: {theme.name}")
    row += 1
    stdscr.addstr(row, 0, f"Description: {theme.description}")
    row += 1
    stdscr.addstr(row, 0, f"Author: {theme.author}")
    row += 2

    # Display sample text with semantic colors
    stdscr.addstr(row, 0, "Semantic Colors:", curses.A_BOLD)
    row += 1
    stdscr.addstr(row, 0, "-" * 60)
    row += 1

    stdscr.addstr(row, 0, "Primary: ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row, 10, "Main UI highlights and focus", curses.color_pair(theme.colors.primary)
    )
    row += 1

    stdscr.addstr(row, 0, "Success: ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row,
        10,
        "Operation completed successfully",
        curses.color_pair(theme.colors.success),
    )
    row += 1

    stdscr.addstr(row, 0, "Error:   ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row, 10, "Critical error occurred", curses.color_pair(theme.colors.error)
    )
    row += 1

    stdscr.addstr(row, 0, "Warning: ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row, 10, "Proceed with caution", curses.color_pair(theme.colors.warning)
    )
    row += 1

    stdscr.addstr(row, 0, "Info:    ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row, 10, "Additional information", curses.color_pair(theme.colors.info)
    )
    row += 1

    stdscr.addstr(row, 0, "Accent:  ", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(
        row, 10, "Secondary highlights", curses.color_pair(theme.colors.accent)
    )
    row += 2

    # Draw a themed box
    stdscr.addstr(row, 0, "Themed Box:", curses.A_BOLD)
    row += 1

    box_y = row
    box_x = 2
    box_height = 5
    box_width = 50

    theme.draw_box(stdscr, box_y, box_x, box_height, box_width, title="Sample Panel")

    # Add content inside the box
    # theme.colors.X returns a color pair NUMBER - must wrap in curses.color_pair()
    stdscr.addstr(
        box_y + 1,
        box_x + 2,
        "This is a themed border box",
        curses.color_pair(theme.colors.foreground),
    )
    stdscr.addstr(
        box_y + 2,
        box_x + 2,
        "with custom Solarized colors",
        curses.color_pair(theme.colors.accent),
    )

    row += box_height + 2

    # Instructions
    stdscr.addstr(row, 0, "-" * 60)
    row += 1
    stdscr.addstr(row, 0, "Press any key to exit", curses.color_pair(theme.colors.info))

    # Refresh and wait for input
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    # Use curses.wrapper() for proper terminal initialization and cleanup
    curses.wrapper(main)
