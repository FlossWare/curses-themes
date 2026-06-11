#!/usr/bin/env python3
import curses
from curses_themes import ThemeManager

def show_theme(stdscr, theme_name):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    
    stdscr.clear()
    theme = ThemeManager.load(theme_name)
    theme.apply(stdscr)
    
    height, width = stdscr.getmaxyx()
    
    title = f"Theme: {theme_name}"
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
    
    theme.draw_box(stdscr, row, 2, 8, 50, title="Themed Panel")
    stdscr.addstr(row + 2, 4, f"Theme: {theme_name}", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(row + 3, 4, "Lightweight theme support for curses", curses.color_pair(theme.colors.foreground))
    stdscr.addstr(row + 5, 4, "Press 'n' for next theme, 'q' to quit", curses.color_pair(theme.colors.accent))
    
    stdscr.refresh()

def main(stdscr):
    themes = ['dark', 'default', 'ti-99-4a', 'trs-80', 'dos', 'dbase-iii', 'borland-3d']
    idx = 0
    
    while True:
        show_theme(stdscr, themes[idx])
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key == ord('n'):
            idx = (idx + 1) % len(themes)

if __name__ == "__main__":
    curses.wrapper(main)
