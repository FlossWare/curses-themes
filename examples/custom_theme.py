#!/usr/bin/env python3
"""
Example demonstrating how to create a custom theme.

This example shows how to:
- Define a custom theme class (SolarizedDarkTheme)
- Implement get_color_map() with Solarized color palette
- Register the theme with ThemeManager
- Load and apply the custom theme
- Display sample text using theme colors
- Use curses.wrapper() for proper terminal handling

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
from curses_themes import Theme, ThemeManager


class SolarizedDarkTheme(Theme):
    """
    Custom theme based on the Solarized Dark color scheme.

    Solarized is a sixteen color palette designed by Ethan Schoonover
    for use with terminal and GUI applications. It features carefully
    chosen colors that reduce eye strain.

    See: https://ethanschoonover.com/solarized/
    """

    def __init__(self):
        """Initialize the Solarized Dark theme."""
        super().__init__(
            name="Solarized Dark",
            description="Professional dark theme with carefully balanced colors",
            author="FlossWare",
        )

    def get_color_map(self):
        """
        Return Solarized Dark color palette.

        Returns:
            Dictionary mapping semantic color names to RGB tuples.
            Each RGB value is in range 0-255.
        """
        # Solarized base colors
        base03 = (0, 43, 54)  # Dark background
        base02 = (7, 54, 66)  # Darker background highlights
        base01 = (88, 110, 117)  # Content tone (comments)
        base00 = (101, 123, 131)  # Body text
        base0 = (131, 148, 150)  # Primary content
        base1 = (147, 161, 161)  # Optional emphasized content
        base2 = (238, 232, 213)  # Background highlights
        base3 = (253, 246, 227)  # Light background

        # Solarized accent colors
        yellow = (181, 137, 0)
        orange = (203, 75, 22)
        red = (220, 50, 47)
        magenta = (211, 54, 130)
        violet = (108, 113, 196)
        blue = (38, 139, 210)
        cyan = (42, 161, 152)
        green = (133, 153, 0)

        return {
            "background": base03,  # Dark background
            "foreground": base0,  # Primary text
            "primary": blue,  # Main UI highlights
            "success": green,  # Positive feedback
            "error": red,  # Error messages
            "warning": yellow,  # Warnings
            "info": cyan,  # Information
            "accent": violet,  # Secondary highlights
        }


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
    ThemeManager.register(SolarizedDarkTheme)

    # Load and apply the custom theme
    theme = ThemeManager.load("solarized-dark")
    theme.apply(stdscr)

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
    stdscr.addstr(
        box_y + 1, box_x + 2, "This is a themed border box", theme.colors.foreground
    )
    stdscr.addstr(
        box_y + 2, box_x + 2, "with custom Solarized colors", theme.colors.accent
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
