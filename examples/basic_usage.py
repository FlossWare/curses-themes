#!/usr/bin/env python3
"""
Basic usage example for curses-themes.

This example demonstrates how to use the theme system with semantic colors
to create a simple themed curses application.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
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
    try:
        theme = ThemeManager.load("default")
        theme.apply(stdscr)
    except RuntimeError as e:
        # Terminal doesn't support colors or theme init failed
        stdscr.addstr(0, 0, f"Theme error: {e}")
        stdscr.addstr(1, 0, "This terminal may not support colors.")
        stdscr.refresh()
        stdscr.getch()
        return
    except Exception as e:
        # Unknown error
        stdscr.addstr(0, 0, f"Error loading theme: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    # Get window dimensions
    height, width = stdscr.getmaxyx()

    # Display title
    title = "curses-themes Basic Example"
    stdscr.addstr(
        0,
        (width - len(title)) // 2,
        title,
        curses.color_pair(theme.colors.primary) | curses.A_BOLD,
    )

    # Display semantic color examples
    y_pos = 2
    stdscr.addstr(
        y_pos,
        2,
        "Semantic Color Examples:",
        curses.color_pair(theme.colors.foreground) | curses.A_BOLD,
    )

    y_pos += 2
    stdscr.addstr(
        y_pos,
        4,
        "Primary: Main UI highlights and focus",
        curses.color_pair(theme.colors.primary),
    )

    y_pos += 1
    stdscr.addstr(
        y_pos,
        4,
        "Success: Operation completed successfully!",
        curses.color_pair(theme.colors.success),
    )

    y_pos += 1
    stdscr.addstr(
        y_pos, 4, "Error: Something went wrong!", curses.color_pair(theme.colors.error)
    )

    y_pos += 1
    stdscr.addstr(
        y_pos,
        4,
        "Warning: Proceed with caution",
        curses.color_pair(theme.colors.warning),
    )

    y_pos += 1
    stdscr.addstr(
        y_pos, 4, "Info: Helpful information here", curses.color_pair(theme.colors.info)
    )

    y_pos += 1
    stdscr.addstr(
        y_pos, 4, "Accent: Secondary highlights", curses.color_pair(theme.colors.accent)
    )

    # Draw a themed box with title
    box_y = y_pos + 3
    box_x = 4
    box_height = 8
    box_width = width - 8

    theme.draw_box(
        stdscr, box_y, box_x, box_height, box_width, title="Themed Border Box"
    )

    # Add content inside the box
    content_y = box_y + 2
    content_x = box_x + 2

    stdscr.addstr(
        content_y,
        content_x,
        "This box demonstrates themed borders and styling.",
        curses.color_pair(theme.colors.foreground),
    )

    stdscr.addstr(
        content_y + 2,
        content_x,
        "Themes provide consistent visual appearance across",
        curses.color_pair(theme.colors.foreground),
    )

    stdscr.addstr(
        content_y + 3,
        content_x,
        "your entire curses application.",
        curses.color_pair(theme.colors.foreground),
    )

    # Display instructions at the bottom
    instructions = "Press any key to quit"
    try:
        stdscr.addstr(
            height - 2,
            (width - len(instructions)) // 2,
            instructions,
            curses.color_pair(theme.colors.info) | curses.A_DIM,
        )
    except curses.error:
        # Ignore errors when drawing at screen boundaries
        pass

    # Refresh and wait for keypress
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
