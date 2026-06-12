#!/usr/bin/env python3
"""
Demo of retro themes ported from curses-java.

Showcases the TI-99/4A, TRS-80, DOS, dBASE III, and dBASE IV themes.

Press any key to cycle through themes, 'q' to quit.
"""

import curses
from curses_themes import ThemeManager


def draw_demo_ui(stdscr, theme):
    """Draw a sample UI using the current theme."""
    height, width = stdscr.getmaxyx()

    # Clear screen
    stdscr.clear()

    # Title
    title = f"Theme: {theme.name}"
    stdscr.addstr(
        0,
        (width - len(title)) // 2,
        title,
        curses.color_pair(theme.components.button_focused) | curses.A_BOLD,
    )

    # Description
    if theme.description:
        desc_lines = theme.description.split("\n")
        for i, line in enumerate(desc_lines[:2]):  # Show first 2 lines
            if len(line) > width - 4:
                line = line[: width - 7] + "..."
            stdscr.addstr(
                2 + i, 2, line, curses.color_pair(theme.components.foreground)
            )

    # Sample buttons
    y = 5
    stdscr.addstr(y, 4, "[ Normal Button ]", curses.color_pair(theme.components.button))
    stdscr.addstr(
        y + 1,
        4,
        "[ Focused Button ]",
        curses.color_pair(theme.components.button_focused) | curses.A_BOLD,
    )

    # Sample text input
    y += 3
    stdscr.addstr(y, 4, "Text Input: ", curses.color_pair(theme.components.foreground))
    stdscr.addstr(y, 16, "Type here...", curses.color_pair(theme.components.text_input))

    # Sample selection
    y += 2
    stdscr.addstr(
        y,
        4,
        "Selected Item",
        curses.color_pair(theme.components.selection) | curses.A_BOLD,
    )
    stdscr.addstr(
        y + 1, 4, "Normal Item", curses.color_pair(theme.components.foreground)
    )

    # Semantic colors (if available)
    y += 3
    stdscr.addstr(
        y, 4, "Semantic Colors:", curses.color_pair(theme.components.foreground)
    )
    y += 1
    try:
        stdscr.addstr(y, 6, "✓ Success", curses.color_pair(theme.colors.success))
        y += 1
        stdscr.addstr(y, 6, "✗ Error", curses.color_pair(theme.colors.error))
        y += 1
        stdscr.addstr(y, 6, "⚠ Warning", curses.color_pair(theme.colors.warning))
        y += 1
        stdscr.addstr(y, 6, "ℹ Info", curses.color_pair(theme.colors.info))
    except Exception:
        # Fallback for terminals without Unicode support
        stdscr.addstr(y, 6, "* Success", curses.color_pair(theme.colors.success))
        y += 1
        stdscr.addstr(y, 6, "* Error", curses.color_pair(theme.colors.error))
        y += 1
        stdscr.addstr(y, 6, "* Warning", curses.color_pair(theme.colors.warning))
        y += 1
        stdscr.addstr(y, 6, "* Info", curses.color_pair(theme.colors.info))

    # Draw a themed box
    if height > 20 and width > 50:
        theme.draw_box(stdscr, height - 8, 2, 6, width - 4, title="Themed Border")
        stdscr.addstr(
            height - 6,
            4,
            "Border style:",
            curses.color_pair(theme.components.foreground),
        )
        border_chars = theme.get_border_chars()
        stdscr.addstr(
            height - 5,
            4,
            f"  {border_chars}",
            curses.color_pair(theme.components.border),
        )

    # Instructions
    instructions = "Press any key for next theme, 'q' to quit"
    stdscr.addstr(
        height - 2,
        (width - len(instructions)) // 2,
        instructions,
        curses.color_pair(theme.components.foreground),
    )

    stdscr.refresh()


def main(stdscr):
    """Main demo loop."""
    # Retro themes from curses-java
    theme_names = [
        "ti-99-4a",  # Texas Instruments TI-99/4A (1981-1984)
        "trs-80",  # Tandy/Radio Shack TRS-80 (1980-1983)
        "dos",  # MS-DOS (1981-1995)
        "dbase-iii",  # dBASE III (1984-1985)
        "dbase-iv",  # dBASE IV (1988-1993)
    ]

    current_idx = 0

    while True:
        # Load and apply current theme
        theme = ThemeManager.load(theme_names[current_idx])
        theme.apply(stdscr)

        # Draw the UI
        draw_demo_ui(stdscr, theme)

        # Wait for keypress
        key = stdscr.getch()

        # Check for quit
        if key == ord("q") or key == ord("Q"):
            break

        # Move to next theme
        current_idx = (current_idx + 1) % len(theme_names)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
