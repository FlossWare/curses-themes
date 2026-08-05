#!/usr/bin/env python3
"""Simple demo cycling through all registered themes."""

import curses
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from curses_themes import ThemeManager


def show_theme(stdscr, name: str):
    theme = ThemeManager.load(name)
    theme.apply(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, f"Theme: {name}", curses.color_pair(theme.colors.primary))
    stdscr.addstr(2, 0, "Success", curses.color_pair(theme.colors.success))
    stdscr.addstr(3, 0, "Error", curses.color_pair(theme.colors.error))
    stdscr.addstr(4, 0, "Warning", curses.color_pair(theme.colors.warning))
    theme.draw_box(stdscr, 6, 2, 6, 40, title=name)
    stdscr.addstr(
        14,
        0,
        "Press 'n' for next theme, 'q' to quit",
        curses.color_pair(theme.colors.accent),
    )
    stdscr.refresh()


def main(stdscr):
    themes = sorted(ThemeManager.list_themes().keys())
    idx = 0

    while True:
        show_theme(stdscr, themes[idx])
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == ord("n"):
            idx = (idx + 1) % len(themes)


if __name__ == "__main__":
    curses.wrapper(main)
