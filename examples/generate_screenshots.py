#!/usr/bin/env python3
"""
Screenshot generator for all themes.

Generates ASCII text screenshots (.txt files) showing each theme's appearance
in a standardized layout. Does NOT require a real terminal or curses -- renders
entirely in-memory so it works in headless environments, CI pipelines, and
SSH sessions without a TTY.

Each screenshot is an 80x25 character grid that demonstrates:
  - Theme name and description
  - Border style with a sample panel
  - Buttons (normal and focused)
  - Text input fields
  - Selection / highlighting
  - Semantic colors (success, error, warning, info)
  - Color palette RGB values
  - 3D effects for Theme3D subclasses (shadow, highlight, lowlight)
  - Retro / vintage aesthetic annotations

Usage:
    python3 generate_screenshots.py [--output-dir DIR]

Copyright (C) 2024 FlossWare
License: GPL-3.0
"""

import argparse
import sys
from pathlib import Path

# Ensure the parent package is importable when running as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from curses_themes import ThemeManager
from curses_themes.theme3d import Theme3D


# ---------------------------------------------------------------------------
# ASCII canvas helper
# ---------------------------------------------------------------------------

class AsciiCanvas:
    """Simple 2-D character buffer for composing text screenshots."""

    def __init__(self, width: int = 80, height: int = 25):
        self.width = width
        self.height = height
        self.grid = [[' '] * width for _ in range(height)]

    def put(self, row: int, col: int, text: str) -> None:
        """Write *text* starting at (row, col), clipping to canvas bounds."""
        if row < 0 or row >= self.height:
            return
        for i, ch in enumerate(text):
            c = col + i
            if 0 <= c < self.width:
                self.grid[row][c] = ch

    def hline(self, row: int, col: int, char: str, length: int) -> None:
        """Draw a horizontal line of *char* repeated *length* times."""
        self.put(row, col, char * length)

    def vline(self, row: int, col: int, char: str, length: int) -> None:
        """Draw a vertical line of *char* repeated *length* times."""
        for i in range(length):
            self.put(row + i, col, char)

    def box(self, row: int, col: int, height: int, width: int,
            border_chars: str, title: str = "") -> None:
        """Draw a bordered box using an 8-character border string (TL T TR L R BL B BR)."""
        if len(border_chars) != 8:
            border_chars = "+-+||+-+"
        tl, t, tr, l, r, bl, b, br = border_chars

        # Corners
        self.put(row, col, tl)
        self.put(row, col + width - 1, tr)
        self.put(row + height - 1, col, bl)
        self.put(row + height - 1, col + width - 1, br)

        # Horizontal edges
        self.hline(row, col + 1, t, width - 2)
        self.hline(row + height - 1, col + 1, b, width - 2)

        # Vertical edges
        self.vline(row + 1, col, l, height - 2)
        self.vline(row + 1, col + width - 1, r, height - 2)

        # Title
        if title and width > len(title) + 4:
            label = f" {title} "
            tx = col + (width - len(label)) // 2
            self.put(row, tx, label)

    def render(self) -> str:
        """Return the canvas as a single string with trailing whitespace stripped."""
        lines = [''.join(row).rstrip() for row in self.grid]
        # Remove trailing blank lines
        while lines and not lines[-1]:
            lines.pop()
        return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def rgb_to_hex(rgb: tuple) -> str:
    """Convert an (R,G,B) tuple to a hex string like #RRGGBB."""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def describe_color(rgb: tuple) -> str:
    """Return a short human-readable name for common terminal colors."""
    known = {
        (0, 0, 0): "Black",
        (255, 255, 255): "White",
        (0, 0, 170): "Blue (CGA)",
        (0, 0, 238): "Blue (VGA)",
        (0, 170, 170): "Cyan (CGA)",
        (0, 205, 205): "Cyan",
        (0, 255, 255): "Cyan (Bright)",
        (255, 255, 85): "Yellow (CGA)",
        (255, 255, 0): "Yellow",
        (205, 205, 0): "Yellow",
        (170, 170, 170): "Light Gray",
        (255, 85, 85): "Light Red",
        (85, 255, 85): "Light Green",
        (170, 0, 170): "Magenta",
        (205, 0, 0): "Red",
        (0, 205, 0): "Green",
        (255, 0, 0): "Red (Bright)",
        (0, 255, 0): "Green (Bright)",
    }
    return known.get(rgb, rgb_to_hex(rgb))


# ---------------------------------------------------------------------------
# Theme screenshot renderer
# ---------------------------------------------------------------------------

def render_theme(theme_name: str) -> str:
    """Render an ASCII text screenshot for the given theme name.

    Returns the screenshot as a multi-line string.
    """
    theme = ThemeManager.load(theme_name)
    color_map = theme.get_color_map()
    border_chars = theme.get_border_chars()
    is_3d = isinstance(theme, Theme3D)

    canvas = AsciiCanvas(80, 25)

    # ------------------------------------------------------------------
    # Row 0: Title bar
    # ------------------------------------------------------------------
    title = theme.name.upper()
    bar = f"={'=' * 2} {title} {'=' * (74 - len(title))}"
    canvas.put(0, 0, bar[:80])

    # ------------------------------------------------------------------
    # Row 1: Description
    # ------------------------------------------------------------------
    desc = theme.description or "(no description)"
    canvas.put(1, 2, desc[:76])

    # ------------------------------------------------------------------
    # Row 3-16: Demo panel
    # ------------------------------------------------------------------
    panel_w = 50
    panel_h = 14
    canvas.box(3, 1, panel_h, panel_w, border_chars, "Sample Panel")

    # 3D shadow hint for 3D themes
    if is_3d:
        shadow_char = chr(0x2591)  # light shade block
        for r in range(panel_h):
            canvas.put(3 + r + 1, 1 + panel_w, shadow_char)
            canvas.put(3 + r + 1, 1 + panel_w + 1, shadow_char)
        for c in range(panel_w + 2):
            canvas.put(3 + panel_h, 1 + 2 + c, shadow_char)

    # Buttons (rows 5-7)
    canvas.put(5, 3, "Buttons:")
    canvas.put(6, 5, "[ Normal Button ]")
    canvas.put(7, 5, "[ FOCUSED BUTTON ]  <-- highlighted")

    # Text input (rows 9-10)
    canvas.put(9, 3, "Text Input:")
    canvas.put(10, 5, "Label: [sample text here______]")

    # Selection (rows 12-15)
    canvas.put(12, 3, "Selection List:")
    canvas.put(13, 5, ">> Selected Item  <<")
    canvas.put(14, 5, "   Normal Item")
    canvas.put(15, 5, "   Normal Item")

    # ------------------------------------------------------------------
    # Row 3-11: Semantic Colors panel (right side)
    # ------------------------------------------------------------------
    sem_x = 53
    sem_w = 26
    sem_h = 9
    canvas.box(3, sem_x, sem_h, sem_w, border_chars, "Semantic Colors")

    canvas.put(5, sem_x + 2, "[OK]  Success message")
    canvas.put(6, sem_x + 2, "[!!]  Error message")
    canvas.put(7, sem_x + 2, "[!?]  Warning message")
    canvas.put(8, sem_x + 2, "[ii]  Info message")
    canvas.put(10, sem_x + 2, "Disabled text (muted)")

    # ------------------------------------------------------------------
    # Row 13-16: Color Palette (right side)
    # ------------------------------------------------------------------
    canvas.put(13, sem_x, "Color Palette (RGB):")
    bg_rgb = color_map.get('background', (0, 0, 0))
    fg_rgb = color_map.get('foreground', (255, 255, 255))
    canvas.put(14, sem_x + 1, f"BG: {rgb_to_hex(bg_rgb)} {describe_color(bg_rgb)}")
    canvas.put(15, sem_x + 1, f"FG: {rgb_to_hex(fg_rgb)} {describe_color(fg_rgb)}")

    primary_rgb = color_map.get('primary', (0, 0, 0))
    canvas.put(16, sem_x + 1, f"Primary: {rgb_to_hex(primary_rgb)}")

    # ------------------------------------------------------------------
    # Row 18-22: Theme metadata / 3D info
    # ------------------------------------------------------------------
    canvas.put(18, 1, f"Border style: {repr(border_chars)}")

    if is_3d:
        canvas.put(19, 1, "3D Effects: ENABLED")
        try:
            shadow = theme.get_shadow_color()
            highlight = theme.get_highlight_color()
            lowlight = theme.get_lowlight_color()
            canvas.put(20, 3, f"Shadow:    fg={rgb_to_hex(shadow.foreground)} bg={rgb_to_hex(shadow.background)}")
            canvas.put(21, 3, f"Highlight: fg={rgb_to_hex(highlight.foreground)} bg={rgb_to_hex(highlight.background)}")
            canvas.put(22, 3, f"Lowlight:  fg={rgb_to_hex(lowlight.foreground)} bg={rgb_to_hex(lowlight.background)}")
        except Exception:
            canvas.put(20, 3, "(3D color details unavailable)")

        # Show 3D raised/sunken demo
        canvas.put(19, 40, "Raised: [##########]")
        canvas.put(20, 40, "Sunken: [..........] (input)")
        # Double-border example
        try:
            dbl = theme.get_double_border_chars()
            canvas.put(21, 40, f"Double border: {repr(dbl)}")
        except Exception:
            pass
    else:
        # Era / aesthetic note
        era = _theme_era(theme_name)
        if era:
            canvas.put(19, 1, f"Era: {era}")

        # Additional color info
        success_rgb = color_map.get('success', (0, 0, 0))
        error_rgb = color_map.get('error', (0, 0, 0))
        warning_rgb = color_map.get('warning', (0, 0, 0))
        info_rgb = color_map.get('info', (0, 0, 0))
        canvas.put(20, 1, f"Success: {rgb_to_hex(success_rgb)}  Error: {rgb_to_hex(error_rgb)}")
        canvas.put(21, 1, f"Warning: {rgb_to_hex(warning_rgb)}  Info:  {rgb_to_hex(info_rgb)}")

        accent_rgb = color_map.get('accent', (0, 0, 0))
        canvas.put(22, 1, f"Accent:  {rgb_to_hex(accent_rgb)}")

    # ------------------------------------------------------------------
    # Row 24: Footer
    # ------------------------------------------------------------------
    footer = f"Theme: {theme.name} | Author: {theme.author or 'FlossWare'} | 3D: {'Yes' if is_3d else 'No'}"
    canvas.put(24, 1, footer[:78])

    return canvas.render()


def _theme_era(name: str) -> str:
    """Return a short era / aesthetic description for well-known themes."""
    eras = {
        "default": "Classic terminal (timeless)",
        "dark": "Modern dark mode aesthetic",
        "light": "Modern high-contrast light mode",
        "ti-99-4a": "Texas Instruments TI-99/4A (1981-1984) -- first 16-bit home computer",
        "trs-80": "Tandy/Radio Shack TRS-80 (1977-1983) -- monochrome phosphor display",
        "dos": "MS-DOS / PC-DOS text mode (1981-1995)",
        "dbase-iii": "Ashton-Tate dBASE III (1984-1985) -- cyan-on-black database UI",
        "dbase-iv": "Ashton-Tate/Borland dBASE IV Control Center (1988-1993)",
        "borland-3d": "Borland Turbo Vision 3D (1990-1997) -- beveled buttons & shadows",
        "dbase-iv-3d": "dBASE IV 3D windowed interface (1988-1993) -- Borland era",
    }
    return eras.get(name, "")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate ASCII text screenshots of all themes"
    )
    parser.add_argument(
        '--output-dir',
        default='screenshots',
        help='Output directory for screenshots (default: screenshots/)'
    )
    args = parser.parse_args()

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    themes = ThemeManager.list_themes()
    generated = []

    print(f"Generating ASCII text screenshots to {output_path}/")
    print(f"Themes found: {len(themes)}")
    print()

    for theme_name in sorted(themes.keys()):
        try:
            screenshot = render_theme(theme_name)
            out_file = output_path / f"{theme_name}.txt"
            out_file.write_text(screenshot + '\n', encoding='utf-8')
            generated.append(str(out_file))
            print(f"  [OK] {out_file}")
        except Exception as exc:
            print(f"  [FAIL] {theme_name}: {exc}", file=sys.stderr)

    print()
    print(f"Generated {len(generated)} of {len(themes)} screenshots.")
    print(f"Output directory: {output_path.resolve()}")
    return generated


if __name__ == "__main__":
    main()
