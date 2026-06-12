#!/usr/bin/env python3
"""
Simple curses-themes demonstration.

This example shows a minimal usage of curses-themes with semantic colors
and themed boxes. Perfect for getting started with the library.

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import curses
from curses_themes import ThemeManager


def main(stdscr):
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    stdscr.clear()

    # Load and apply theme with error handling
    try:
        theme = ThemeManager.load("dark")
        theme.apply(stdscr)
    except RuntimeError as e:
        # Terminal doesn't support colors or theme init failed
        stdscr.addstr(0, 0, f"Theme error: {e}")
        stdscr.refresh()
        stdscr.getch()
        return
    except Exception as e:
        # Unknown error - display and exit
        stdscr.addstr(0, 0, f"Error loading theme: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    height, width = stdscr.getmaxyx()

    title = "curses-themes Demo"
    stdscr.addstr(
        0,
        (width - len(title)) // 2,
        title,
        curses.color_pair(theme.colors.primary) | curses.A_BOLD,
    )

    row = 2
    stdscr.addstr(row, 2, "Semantic Colors:", curses.A_BOLD)
    row += 2

    stdscr.addstr(row, 4, "✓ Success", curses.color_pair(theme.colors.success))
    row += 1
    stdscr.addstr(row, 4, "✗ Error", curses.color_pair(theme.colors.error))
    row += 1
    stdscr.addstr(row, 4, "⚠ Warning", curses.color_pair(theme.colors.warning))
    row += 1
    stdscr.addstr(row, 4, "ℹ Info", curses.color_pair(theme.colors.info))
    row += 2

    theme.draw_box(stdscr, row, 2, 6, 40, title="Themed Panel")
    stdscr.addstr(
        row + 2, 4, "This is a themed box", curses.color_pair(theme.colors.foreground)
    )
    stdscr.addstr(row + 3, 4, "Theme: dark", curses.color_pair(theme.colors.accent))

    stdscr.addstr(height - 2, 2, "Press any key to exit", curses.color_pair(theme.colors.info) | curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
