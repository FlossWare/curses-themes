#!/usr/bin/env python3
"""
Basic usage example for curses-themes.

This example demonstrates how to use the theme system with semantic colors
to create a simple themed curses application.

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


def main(stdscr):
    """
    Main application loop demonstrating themed curses interface.

    Args:
        stdscr: The main curses window object
    """
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # Load and apply the default theme
    theme = ThemeManager.load('default')
    theme.apply(stdscr)

    # Get window dimensions
    height, width = stdscr.getmaxyx()

    # Display title
    title = "curses-themes Basic Example"
    stdscr.addstr(0, (width - len(title)) // 2, title,
                  curses.color_pair(theme.colors.primary) | curses.A_BOLD)

    # Display semantic color examples
    y_pos = 2
    stdscr.addstr(y_pos, 2, "Semantic Color Examples:",
                  curses.color_pair(theme.colors.foreground) | curses.A_BOLD)

    y_pos += 2
    stdscr.addstr(y_pos, 4, "Primary: Main UI highlights and focus",
                  curses.color_pair(theme.colors.primary))

    y_pos += 1
    stdscr.addstr(y_pos, 4, "Success: Operation completed successfully!",
                  curses.color_pair(theme.colors.success))

    y_pos += 1
    stdscr.addstr(y_pos, 4, "Error: Something went wrong!",
                  curses.color_pair(theme.colors.error))

    y_pos += 1
    stdscr.addstr(y_pos, 4, "Warning: Proceed with caution",
                  curses.color_pair(theme.colors.warning))

    y_pos += 1
    stdscr.addstr(y_pos, 4, "Info: Helpful information here",
                  curses.color_pair(theme.colors.info))

    y_pos += 1
    stdscr.addstr(y_pos, 4, "Accent: Secondary highlights",
                  curses.color_pair(theme.colors.accent))

    # Draw a themed box with title
    box_y = y_pos + 3
    box_x = 4
    box_height = 8
    box_width = width - 8

    theme.draw_box(stdscr, box_y, box_x, box_height, box_width,
                   title="Themed Border Box")

    # Add content inside the box
    content_y = box_y + 2
    content_x = box_x + 2

    stdscr.addstr(content_y, content_x,
                  "This box demonstrates themed borders and styling.",
                  curses.color_pair(theme.colors.foreground))

    stdscr.addstr(content_y + 2, content_x,
                  "Themes provide consistent visual appearance across",
                  curses.color_pair(theme.colors.foreground))

    stdscr.addstr(content_y + 3, content_x,
                  "your entire curses application.",
                  curses.color_pair(theme.colors.foreground))

    # Display instructions at the bottom
    instructions = "Press any key to quit"
    try:
        stdscr.addstr(height - 2, (width - len(instructions)) // 2,
                     instructions,
                     curses.color_pair(theme.colors.info) | curses.A_DIM)
    except curses.error:
        # Ignore if too close to bottom edge
        pass

    # Refresh and wait for keypress
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
