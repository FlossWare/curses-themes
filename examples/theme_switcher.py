#!/usr/bin/env python3
"""Interactive theme switcher demo for curses-themes."""

import curses
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from curses_themes import ThemeManager


def draw_theme_demo(stdscr, theme, theme_name: str, theme_index: int, total_themes: int):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = "=== Interactive Theme Switcher ==="
    stdscr.addstr(0, max(0, (width - len(title)) // 2), title, curses.A_BOLD)

    theme_info = f"Theme {theme_index + 1} of {total_themes}: {theme_name}"
    stdscr.addstr(1, max(0, (width - len(theme_info)) // 2), theme_info)

    y = 3
    x_label = 2
    x_sample = 20

    stdscr.addstr(y, x_label, "Semantic colors:", curses.A_BOLD)
    y += 2
    samples = [
        ("Primary", theme.colors.primary),
        ("Success", theme.colors.success),
        ("Error", theme.colors.error),
        ("Warning", theme.colors.warning),
        ("Info", theme.colors.info),
        ("Accent", theme.colors.accent),
    ]
    for label, pair in samples:
        stdscr.addstr(y, x_label, f"{label}:", curses.color_pair(theme.colors.foreground))
        stdscr.addstr(y, x_sample, f"Sample {label}", curses.color_pair(pair))
        y += 1

    y += 1
    stdscr.addstr(y, x_label, "Themed box:")
    y += 1
    theme.draw_box(stdscr, y, x_label, 5, 40, title=theme_name)

    help_line = "Press 'n' next, 'p' previous, 'q' quit"
    stdscr.addstr(height - 2, max(0, (width - len(help_line)) // 2), help_line)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    theme_names = sorted(ThemeManager.list_themes().keys())
    current_index = 0

    try:
        current_theme = ThemeManager.load(theme_names[current_index])
        current_theme.apply(stdscr)
    except Exception as e:
        stdscr.addstr(0, 0, f"Error loading theme: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    while True:
        draw_theme_demo(
            stdscr,
            current_theme,
            theme_names[current_index],
            current_index,
            len(theme_names),
        )
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        if key in (ord("q"), ord("Q")):
            break
        elif key in (ord("n"), ord("N"), curses.KEY_RIGHT):
            current_index = (current_index + 1) % len(theme_names)
        elif key in (ord("p"), ord("P"), curses.KEY_LEFT):
            current_index = (current_index - 1) % len(theme_names)
        else:
            continue

        try:
            current_theme = ThemeManager.load(theme_names[current_index])
            current_theme.apply(stdscr)
        except Exception:
            pass


if __name__ == "__main__":
    curses.wrapper(main)
