#!/usr/bin/env python3
"""
Headless screenshot generator for all themes.

Generates ASCII screenshots without requiring a real terminal.
"""

import argparse
from pathlib import Path

from curses_themes import ThemeManager


def parse_border_chars(border_str):
    """Parse 8-character border string into dict"""
    if len(border_str) != 8:
        border_str = "+-+||+-+"

    return {
        "tl": border_str[0],  # top-left
        "horiz": border_str[1],  # horizontal (top)
        "tr": border_str[2],  # top-right
        "vert": border_str[3],  # vertical (left)
        "right_vert": border_str[4],  # vertical (right)
        "bl": border_str[5],  # bottom-left
        "bottom": border_str[6],  # horizontal (bottom)
        "br": border_str[7],  # bottom-right
    }


def generate_theme_sample(theme_name, width=80, height=30):
    """Generate a text-based sample of a theme without curses"""
    theme = ThemeManager.load(theme_name)

    lines = []

    # Header
    title = f"Theme: {theme.name}"
    lines.append(title.center(width))
    lines.append("=" * width)

    if theme.description:
        # Wrap description if needed
        desc_lines = []
        words = theme.description.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 < width - 2:
                current_line += word + " "
            else:
                desc_lines.append(current_line.rstrip())
                current_line = "  " + word + " "
        if current_line.strip():
            desc_lines.append(current_line.rstrip())

        for line in desc_lines:
            lines.append(line)
    lines.append("")

    # Box border (using theme's border style)
    border_str = theme.get_border_chars()
    bc = parse_border_chars(border_str)
    box_width = 54

    # Sample Panel Box
    lines.append("  " + bc["tl"] + bc["horiz"] * (box_width - 2) + bc["tr"])
    lines.append(
        "  " + bc["vert"] + " Sample Panel".ljust(box_width - 2) + bc["right_vert"]
    )

    # Content separator
    lines.append("  " + bc["vert"] + bc["horiz"] * (box_width - 2) + bc["right_vert"])

    # Buttons
    lines.append("  " + bc["vert"] + "".ljust(box_width - 2) + bc["right_vert"])
    lines.append(
        "  "
        + bc["vert"]
        + "  [ Normal Button ]".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "  [ Focused Button ] <--".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append("  " + bc["vert"] + "".ljust(box_width - 2) + bc["right_vert"])

    # Text input
    lines.append(
        "  "
        + bc["vert"]
        + "  Input: [Type here...             ]".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append("  " + bc["vert"] + "".ljust(box_width - 2) + bc["right_vert"])

    # Selection
    lines.append(
        "  " + bc["vert"] + "  List Items:".ljust(box_width - 2) + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "    > Selected Item (highlighted)".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append(
        "  " + bc["vert"] + "      Normal Item".ljust(box_width - 2) + bc["right_vert"]
    )
    lines.append(
        "  " + bc["vert"] + "      Another Item".ljust(box_width - 2) + bc["right_vert"]
    )
    lines.append("  " + bc["vert"] + "".ljust(box_width - 2) + bc["right_vert"])

    # Semantic colors
    lines.append(
        "  " + bc["vert"] + "  Status Messages:".ljust(box_width - 2) + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "    [OK] Success: Operation completed".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "    [!!] Error: Something went wrong".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "    [/!\\] Warning: Check this carefully".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append(
        "  "
        + bc["vert"]
        + "    [i] Info: Additional details here".ljust(box_width - 2)
        + bc["right_vert"]
    )
    lines.append("  " + bc["vert"] + "".ljust(box_width - 2) + bc["right_vert"])

    # Bottom border
    lines.append("  " + bc["bl"] + bc["bottom"] * (box_width - 2) + bc["br"])
    lines.append("")

    # Theme details
    lines.append("  Theme Details:")
    lines.append("  " + "-" * 50)

    # Border style
    border_name = "ASCII" if bc["horiz"] == "-" else "Unicode Box Drawing"
    lines.append(f"  Border Style:  {border_name}")
    lines.append(f"  Border Chars:  {border_str!r}")

    # Author
    if hasattr(theme, "author") and theme.author:
        lines.append(f"  Author:        {theme.author}")

    # Color info (without needing to apply)
    lines.append("")
    lines.append("  Color Components:")

    components = theme.get_components()

    bg = components.get("background")
    if bg:
        lines.append(f"    Background:    fg={bg.foreground} bg={bg.background}")

    border = components.get("border")
    if border:
        lines.append(
            f"    Border:        fg={border.foreground} bg={border.background}"
        )

    button = components.get("button")
    if button:
        lines.append(
            f"    Button:        fg={button.foreground} bg={button.background}"
        )

    button_f = components.get("button_focused")
    if button_f:
        lines.append(
            f"    Button Focus:  fg={button_f.foreground} bg={button_f.background}"
        )

    # Pad to height
    while len(lines) < height:
        lines.append("")

    return "\n".join(lines[:height])


def create_readme(output_path, themes):
    """Create a README with all theme samples"""
    readme_lines = [
        "# Curses-Themes Screenshot Gallery",
        "",
        "ASCII text screenshots of all available themes.",
        "",
        "## Available Themes",
        "",
    ]

    for theme_name in sorted(themes.keys()):
        theme = ThemeManager.load(theme_name)
        readme_lines.append(f"### {theme.name}")
        if theme.description:
            readme_lines.append(f"_{theme.description}_")
        readme_lines.append("")
        readme_lines.append(f"File: [`{theme_name}.txt`](./{theme_name}.txt)")
        readme_lines.append("")

    readme_lines.extend(
        [
            "## Usage",
            "",
            "These are ASCII text files that can be:",
            "- Viewed directly in any text editor",
            "- Converted to images using screenshot tools",
            "- Used in documentation",
            "- Shared to demonstrate theme appearance",
            "",
            "## Generating Screenshots",
            "",
            "To regenerate these screenshots:",
            "",
            "```bash",
            "python3 examples/generate_screenshots_headless.py --output-dir screenshots/",
            "```",
            "",
        ]
    )

    readme_file = output_path / "README.md"
    readme_file.write_text("\n".join(readme_lines), encoding="utf-8")
    return readme_file


def main():
    """Generate screenshots for all themes"""
    parser = argparse.ArgumentParser(
        description="Generate ASCII screenshots of all themes (headless mode)"
    )
    parser.add_argument(
        "--output-dir",
        default="screenshots",
        help="Output directory for screenshots (default: screenshots/)",
    )
    parser.add_argument(
        "--with-readme",
        action="store_true",
        help="Also generate README.md with theme gallery",
    )

    args = parser.parse_args()

    # Get all themes
    themes = ThemeManager.list_themes()

    # Ensure output directory exists
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating screenshots for all themes...")
    print("This will create ASCII text files showing each theme's appearance.")
    print()

    screenshot_files = []
    for theme_name in sorted(themes.keys()):
        # Generate screenshot
        screenshot = generate_theme_sample(theme_name)

        # Save to file
        output_file = output_path / f"{theme_name}.txt"
        output_file.write_text(screenshot, encoding="utf-8")
        screenshot_files.append(output_file)

        print(f"Generated: {output_file}")

    # Generate README if requested
    if args.with_readme:
        readme_file = create_readme(output_path, themes)
        print(f"\nGenerated: {readme_file}")

    print(f"\nAll screenshots saved to: {output_path.absolute()}")
    print(f"Total themes: {len(themes)}")


if __name__ == "__main__":
    main()
