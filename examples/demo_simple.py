#!/usr/bin/env python3
import curses
from curses_themes import ThemeManager

def main(stdscr):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    
    stdscr.clear()
    theme = ThemeManager.load('dark')
    theme.apply(stdscr)
    
    height, width = stdscr.getmaxyx()
    
    title = "curses-themes Demo"
    stdscr.addstr(0, (width - len(title)) // 2, title,
                  curses.color_pair(theme.colors.primary) | curses.A_BOLD)
    
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
    stdscr.addstr(row + 2, 4, "This is a themed box", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(row + 3, 4, "Theme: dark", curses.color_pair(theme.colors.accent))
    
    stdscr.addstr(height - 2, 2, "Press any key to exit", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
