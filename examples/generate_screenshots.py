#!/usr/bin/env python3
"""
Screenshot generator for all themes.

Generates ASCII screenshots (text files) showing each theme's appearance.
Can be used to create visual documentation or converted to images.

Usage:
    python3 generate_screenshots.py [--output-dir DIR]
"""

import curses
import argparse
from pathlib import Path
from curses_themes import ThemeManager


def capture_theme_screenshot(stdscr, theme_name):
    """Capture a theme's appearance as ASCII text"""
    # Load and apply theme
    theme = ThemeManager.load(theme_name)
    theme.apply(stdscr)

    height, width = stdscr.getmaxyx()

    # Draw sample UI
    stdscr.clear()

    # Title
    title = f"Theme: {theme.name}"
    stdscr.addstr(0, (width - len(title)) // 2, title,
                 curses.color_pair(theme.components.button_focused) | curses.A_BOLD)

    # Description (if short enough)
    if theme.description and len(theme.description) < width - 4:
        stdscr.addstr(1, 2, theme.description[:width-4],
                     curses.color_pair(theme.components.foreground))

    # Sample box with border
    box_y, box_x = 3, 2
    box_height, box_width = min(height - 10, 15), min(width - 4, 50)

    if height > 15 and width > 30:
        theme.draw_box(stdscr, box_y, box_x, box_height, box_width, title="Sample Panel")

        # Content inside box
        content_y = box_y + 1
        content_x = box_x + 2

        # Buttons
        stdscr.addstr(content_y, content_x, "[ Normal Button ]",
                     curses.color_pair(theme.components.button))
        stdscr.addstr(content_y + 1, content_x, "[ Focused Button ]",
                     curses.color_pair(theme.components.button_focused) | curses.A_BOLD)

        # Text input
        stdscr.addstr(content_y + 3, content_x, "Input: ",
                     curses.color_pair(theme.components.foreground))
        stdscr.addstr(content_y + 3, content_x + 7, "Type here...",
                     curses.color_pair(theme.components.text_input))

        # Selection
        stdscr.addstr(content_y + 5, content_x, "* Selected Item",
                     curses.color_pair(theme.components.selection) | curses.A_BOLD)
        stdscr.addstr(content_y + 6, content_x, "  Normal Item",
                     curses.color_pair(theme.components.foreground))

        # Semantic colors
        stdscr.addstr(content_y + 8, content_x, "Semantic Colors:",
                     curses.color_pair(theme.components.foreground))
        stdscr.addstr(content_y + 9, content_x + 2, "Success message",
                     curses.color_pair(theme.colors.success))
        stdscr.addstr(content_y + 10, content_x + 2, "Error message",
                     curses.color_pair(theme.colors.error))
        stdscr.addstr(content_y + 11, content_x + 2, "Warning message",
                     curses.color_pair(theme.colors.warning))
        stdscr.addstr(content_y + 12, content_x + 2, "Info message",
                     curses.color_pair(theme.colors.info))

    # Border style indicator
    if height > 20:
        border_y = height - 3
        border_text = f"Border: {theme.get_border_chars()}"
        stdscr.addstr(border_y, 2, border_text,
                     curses.color_pair(theme.components.foreground))

    stdscr.refresh()

    # Capture screen contents as text
    lines = []
    for y in range(min(height, 25)):  # Limit height for readability
        line = ""
        for x in range(min(width, 80)):  # Limit width for readability
            try:
                char = stdscr.instr(y, x, 1).decode('utf-8', errors='ignore')
                line += char if char.isprintable() else ' '
            except:
                line += ' '
        lines.append(line.rstrip())

    return '\n'.join(lines)


def main(stdscr, output_dir):
    """Generate screenshots for all themes"""
    curses.curs_set(0)  # Hide cursor

    # Get all themes
    themes = ThemeManager.list_themes()

    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for theme_name in sorted(themes.keys()):
        # Generate screenshot
        screenshot = capture_theme_screenshot(stdscr, theme_name)

        # Save to file
        output_file = output_path / f"{theme_name}.txt"
        output_file.write_text(screenshot, encoding='utf-8')

        print(f"Generated: {output_file}")

    print(f"\nAll screenshots saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate ASCII screenshots of all themes"
    )
    parser.add_argument(
        '--output-dir',
        default='screenshots',
        help='Output directory for screenshots (default: screenshots/)'
    )

    args = parser.parse_args()

    print("Generating screenshots for all themes...")
    print("This will create ASCII text files showing each theme's appearance.")
    print()

    curses.wrapper(main, args.output_dir)

    print()
    print("To convert to images:")
    print("  - Use a screenshot tool on your terminal")
    print("  - Or use tools like 'convert' from ImageMagick")
    print("  - Or use online services like carbon.now.sh")
