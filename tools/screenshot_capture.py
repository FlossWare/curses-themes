#!/usr/bin/env python3
"""
Screenshot capture tool for curses-themes library using PIL/Pillow.

Generates pixel-perfect PNG screenshots of all themes by directly rendering
terminal output to images. This approach provides consistent, automated
screenshot generation without requiring actual terminal emulators.

Design:
    - Pure Python using PIL/Pillow for image rendering
    - Monospace font rendering for authentic terminal appearance
    - Direct RGB color mapping from theme definitions
    - Unicode box-drawing character support
    - Consistent 800x600px layout for all themes
    - Special 3D rendering for themes with shadow/bevel effects

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from PIL import Image, ImageDraw, ImageFont

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from curses_themes import ThemeManager
from curses_themes.theme import Theme, ColorPair
from curses_themes.theme3d import Theme3D


class TerminalRenderer:
    """
    Renders terminal output to PNG images using PIL.

    This class simulates a terminal display by drawing characters in a monospace
    font on a pixel canvas. It handles color mapping, Unicode characters, and
    provides a curses-like API for positioning and styling text.

    Attributes:
        width: Terminal width in characters (default: 80)
        height: Terminal height in characters (default: 24)
        char_width: Character cell width in pixels
        char_height: Character cell height in pixels
        font_size: Font size in points
        padding: Border padding in pixels
    """

    def __init__(
        self,
        width: int = 80,
        height: int = 24,
        font_size: int = 14,
        padding: int = 10
    ):
        """
        Initialize terminal renderer.

        Args:
            width: Terminal width in characters
            height: Terminal height in characters
            font_size: Font size in points
            padding: Border padding in pixels
        """
        self.width = width
        self.height = height
        self.font_size = font_size
        self.padding = padding

        # Load monospace font
        self.font = self._load_font()

        # Calculate character cell dimensions
        # Use a test character to measure actual dimensions
        test_img = Image.new('RGB', (100, 100), (0, 0, 0))
        test_draw = ImageDraw.Draw(test_img)
        bbox = test_draw.textbbox((0, 0), 'M', font=self.font)
        self.char_width = bbox[2] - bbox[0]
        self.char_height = bbox[3] - bbox[1]

        # Calculate image dimensions
        self.img_width = self.width * self.char_width + 2 * self.padding
        self.img_height = self.height * self.char_height + 2 * self.padding

        # Initialize image and drawing context
        self.image = None
        self.draw = None
        self.current_bg = (0, 0, 0)
        self.current_fg = (255, 255, 255)

    def _load_font(self) -> ImageFont.FreeTypeFont:
        """
        Load a monospace font for terminal rendering.

        Tries multiple common monospace fonts in order of preference.
        Falls back to default PIL font if none are found.

        Returns:
            ImageFont instance
        """
        # Try common monospace fonts
        font_paths = [
            # DejaVu Sans Mono (most common)
            '/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            # Liberation Mono
            '/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            # Noto Sans Mono
            '/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf',
            '/usr/share/fonts/noto/NotoSansMono-Regular.ttf',
            # Nimbus Mono
            '/usr/share/fonts/urw-base35/NimbusMonoPS-Regular.otf',
            # Courier
            '/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf',
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, self.font_size)
                except Exception:
                    continue

        # Fall back to default font
        print("Warning: No monospace font found, using default font", file=sys.stderr)
        return ImageFont.load_default()

    def clear(self, bg_color: Tuple[int, int, int] = (0, 0, 0)):
        """
        Clear the screen with the given background color.

        Args:
            bg_color: RGB background color tuple
        """
        self.image = Image.new('RGB', (self.img_width, self.img_height), bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.current_bg = bg_color

    def _char_to_pixel(self, y: int, x: int) -> Tuple[int, int]:
        """
        Convert character coordinates to pixel coordinates.

        Args:
            y: Row (0-indexed)
            x: Column (0-indexed)

        Returns:
            Tuple of (pixel_x, pixel_y)
        """
        pixel_x = x * self.char_width + self.padding
        pixel_y = y * self.char_height + self.padding
        return pixel_x, pixel_y

    def addstr(
        self,
        y: int,
        x: int,
        text: str,
        fg_color: Optional[Tuple[int, int, int]] = None,
        bg_color: Optional[Tuple[int, int, int]] = None,
        bold: bool = False
    ):
        """
        Add a string at the given position.

        Args:
            y: Row (0-indexed)
            x: Column (0-indexed)
            text: Text to draw
            fg_color: Foreground RGB color (uses current if None)
            bg_color: Background RGB color (uses current if None)
            bold: Whether to render text in bold
        """
        if fg_color is None:
            fg_color = self.current_fg
        if bg_color is None:
            bg_color = self.current_bg

        pixel_x, pixel_y = self._char_to_pixel(y, x)

        # Draw background for the text area
        text_width = len(text) * self.char_width
        self.draw.rectangle(
            [pixel_x, pixel_y, pixel_x + text_width, pixel_y + self.char_height],
            fill=bg_color
        )

        # Draw text
        font = self.font
        if bold:
            # Simulate bold by drawing text twice with slight offset
            self.draw.text((pixel_x, pixel_y), text, font=font, fill=fg_color)
            self.draw.text((pixel_x + 1, pixel_y), text, font=font, fill=fg_color)
        else:
            self.draw.text((pixel_x, pixel_y), text, font=font, fill=fg_color)

    def addch(
        self,
        y: int,
        x: int,
        char: str,
        fg_color: Optional[Tuple[int, int, int]] = None,
        bg_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        Add a single character at the given position.

        Args:
            y: Row (0-indexed)
            x: Column (0-indexed)
            char: Character to draw
            fg_color: Foreground RGB color
            bg_color: Background RGB color
        """
        self.addstr(y, x, char, fg_color, bg_color)

    def fill_rect(
        self,
        y: int,
        x: int,
        height: int,
        width: int,
        bg_color: Tuple[int, int, int]
    ):
        """
        Fill a rectangular area with a background color.

        Args:
            y: Top-left row
            x: Top-left column
            height: Height in characters
            width: Width in characters
            bg_color: RGB background color
        """
        pixel_x, pixel_y = self._char_to_pixel(y, x)
        pixel_width = width * self.char_width
        pixel_height = height * self.char_height

        self.draw.rectangle(
            [pixel_x, pixel_y, pixel_x + pixel_width, pixel_y + pixel_height],
            fill=bg_color
        )

    def draw_shadow(
        self,
        y: int,
        x: int,
        height: int,
        width: int,
        shadow_color: Tuple[int, int, int],
        offset_x: int = 2,
        offset_y: int = 1
    ):
        """
        Draw a drop shadow behind a rectangular element.

        Renders shadow strips on the right and bottom edges of a box to
        create a 3D depth illusion, matching the shadow rendering behavior
        from Theme3D.draw_box_3d().

        Args:
            y: Top-left row of the box (not the shadow)
            x: Top-left column of the box (not the shadow)
            height: Box height in characters
            width: Box width in characters
            shadow_color: RGB color for the shadow
            offset_x: Horizontal shadow offset in characters (default: 2)
            offset_y: Vertical shadow offset in characters (default: 1)
        """
        shadow_y = y + offset_y
        shadow_x = x + offset_x

        # Right edge shadow strip
        if offset_x > 0:
            self.fill_rect(shadow_y, x + width, height, offset_x, shadow_color)

        # Bottom edge shadow strip (extends full width including offset)
        if offset_y > 0:
            self.fill_rect(y + height, shadow_x, offset_y, width, shadow_color)

    def draw_box(
        self,
        y: int,
        x: int,
        height: int,
        width: int,
        border_chars: str,
        fg_color: Tuple[int, int, int],
        bg_color: Tuple[int, int, int],
        title: str = ""
    ):
        """
        Draw a box with borders.

        Args:
            y: Top-left row
            x: Top-left column
            height: Box height in characters
            width: Box width in characters
            border_chars: 8-character string (TL, T, TR, L, R, BL, B, BR)
            fg_color: Border foreground color
            bg_color: Border background color
            title: Optional title text
        """
        if len(border_chars) != 8:
            raise ValueError(f"border_chars must be 8 characters, got {len(border_chars)}")

        tl, t, tr, l, r, bl, b, br = border_chars

        # Draw corners
        self.addstr(y, x, tl, fg_color, bg_color)
        self.addstr(y, x + width - 1, tr, fg_color, bg_color)
        self.addstr(y + height - 1, x, bl, fg_color, bg_color)
        self.addstr(y + height - 1, x + width - 1, br, fg_color, bg_color)

        # Draw horizontal borders
        for i in range(1, width - 1):
            self.addstr(y, x + i, t, fg_color, bg_color)
            self.addstr(y + height - 1, x + i, b, fg_color, bg_color)

        # Draw vertical borders
        for i in range(1, height - 1):
            self.addstr(y + i, x, l, fg_color, bg_color)
            self.addstr(y + i, x + width - 1, r, fg_color, bg_color)

        # Draw title if provided
        if title and width > len(title) + 4:
            title_text = f" {title} "
            title_x = x + (width - len(title_text)) // 2
            self.addstr(y, title_x, title_text, fg_color, bg_color)

    def save(self, filepath: str):
        """
        Save the rendered image to a file.

        Args:
            filepath: Output file path (PNG format)
        """
        if self.image is None:
            raise RuntimeError("No image to save. Call clear() first.")

        self.image.save(filepath, 'PNG')


def render_theme_screenshot(theme: Theme, renderer: TerminalRenderer) -> Image.Image:
    """
    Render a complete theme screenshot.

    Creates a standardized layout showing all theme features:
    - Theme name and description
    - Demo panel with buttons, inputs, selections
    - Semantic colors (success, error, warning, info)
    - Border style demonstration
    - For 3D themes: shadow and bevel effects

    Args:
        theme: Theme instance to render
        renderer: TerminalRenderer instance

    Returns:
        PIL Image instance
    """
    # Get theme colors
    color_map = theme.get_color_map()
    bg_color = color_map.get('background', (0, 0, 0))
    fg_color = color_map.get('foreground', (255, 255, 255))
    primary_color = color_map.get('primary', (0, 120, 215))
    success_color = color_map.get('success', (16, 124, 16))
    error_color = color_map.get('error', (232, 17, 35))
    warning_color = color_map.get('warning', (193, 156, 0))
    info_color = color_map.get('info', (0, 120, 212))

    # Get component colors (with fallbacks)
    try:
        button_bg = theme.get_button()
        if button_bg is None:
            button_fg, button_bg = primary_color, bg_color
        else:
            button_fg, button_bg = button_bg.foreground, button_bg.background
    except:
        button_fg, button_bg = primary_color, bg_color

    try:
        button_focused = theme.get_button_focused()
        if button_focused is None:
            focused_fg, focused_bg = bg_color, primary_color
        else:
            focused_fg, focused_bg = button_focused.foreground, button_focused.background
    except:
        focused_fg, focused_bg = bg_color, primary_color

    try:
        text_input = theme.get_text_input()
        if text_input is None:
            input_fg, input_bg = success_color, bg_color
        else:
            input_fg, input_bg = text_input.foreground, text_input.background
    except:
        input_fg, input_bg = success_color, bg_color

    try:
        selection = theme.get_selection()
        if selection is None:
            select_fg, select_bg = bg_color, fg_color
        else:
            select_fg, select_bg = selection.foreground, selection.background
    except:
        select_fg, select_bg = bg_color, fg_color

    try:
        border = theme.get_border()
        if border is None:
            border_fg, border_bg = fg_color, bg_color
        else:
            border_fg, border_bg = border.foreground, border.background
    except:
        border_fg, border_bg = fg_color, bg_color

    # Clear screen with background color
    renderer.clear(bg_color)

    # Row 0: Theme name (centered, bold, in focused button colors)
    title = f"═══════════ {theme.name.upper()} ═══════════"
    title_x = (renderer.width - len(title)) // 2
    renderer.addstr(0, title_x, title, focused_fg, focused_bg, bold=True)

    # Row 1: Theme description
    desc = theme.description[:renderer.width - 4] if theme.description else ""
    if desc:
        renderer.addstr(1, 2, desc, fg_color, bg_color)

    # Row 3-17: Main demo panel
    border_chars = theme.get_border_chars()

    # Draw main demo panel background
    renderer.fill_rect(3, 2, 15, 54, bg_color)
    renderer.draw_box(3, 2, 15, 54, border_chars, border_fg, border_bg, "DEMO PANEL")

    # Draw shadow behind demo panel for 3D themes
    if isinstance(theme, Theme3D):
        try:
            shadow = theme.get_shadow_color()
            # For better visibility, use a darker version of the background instead of pure black
            if shadow and shadow.foreground:
                shadow_color = shadow.foreground
            else:
                # Use 50% darker background color for better contrast
                shadow_color = tuple(max(0, int(c * 0.5)) for c in bg_color)
            renderer.draw_shadow(3, 2, 15, 54, shadow_color,
                                 theme.shadow_offset_x, theme.shadow_offset_y)
        except Exception:
            pass

    # Buttons (rows 5-7)
    renderer.addstr(5, 4, "Buttons:", fg_color, bg_color)
    renderer.addstr(6, 6, "[ Normal Button ]", button_fg, button_bg)
    renderer.addstr(7, 6, "[ FOCUSED BUTTON ]", focused_fg, focused_bg, bold=True)

    # Text Input (rows 9-10)
    renderer.addstr(9, 4, "Text Input:", fg_color, bg_color)
    renderer.addstr(10, 6, "Input: ", fg_color, bg_color)
    renderer.addstr(10, 13, "[sample text here____]", input_fg, input_bg)

    # Selection (rows 12-15)
    renderer.addstr(12, 4, "Selection:", fg_color, bg_color)
    renderer.addstr(13, 6, "▶ Selected Item", select_fg, select_bg, bold=True)
    renderer.addstr(14, 6, "  Normal Item", fg_color, bg_color)
    renderer.addstr(15, 6, "  Normal Item", fg_color, bg_color)

    # Row 3-11: Semantic colors panel
    renderer.draw_box(3, 58, 9, 22, border_chars, border_fg, border_bg, "COLORS")

    # Draw shadow behind colors panel for 3D themes
    if isinstance(theme, Theme3D):
        try:
            shadow = theme.get_shadow_color()
            # For better visibility, use a darker version of the background instead of pure black
            if shadow and shadow.foreground:
                shadow_color = shadow.foreground
            else:
                # Use 50% darker background color for better contrast
                shadow_color = tuple(max(0, int(c * 0.5)) for c in bg_color)
            renderer.draw_shadow(3, 58, 9, 22, shadow_color,
                                 theme.shadow_offset_x, theme.shadow_offset_y)
        except Exception:
            pass

    renderer.addstr(5, 60, "✓ Success message", success_color, bg_color)
    renderer.addstr(6, 60, "✗ Error message", error_color, bg_color)
    renderer.addstr(7, 60, "⚠ Warning message", warning_color, bg_color)
    renderer.addstr(8, 60, "ℹ Info message", info_color, bg_color)

    # Border style info (row 13-15)
    renderer.addstr(13, 58, "Border Style:", fg_color, bg_color)
    renderer.addstr(14, 60, border_chars, border_fg, bg_color)

    # 3D Effects panel (for 3D themes only)
    if isinstance(theme, Theme3D):
        try:
            shadow = theme.get_shadow_color()
            highlight = theme.get_highlight_color()
            lowlight = theme.get_lowlight_color()

            # For better visibility, use a darker version of the background instead of pure black
            if shadow and shadow.foreground:
                shadow_color = shadow.foreground
            else:
                # Use 50% darker background color for better contrast
                shadow_color = tuple(max(0, int(c * 0.5)) for c in bg_color)
            highlight_color = highlight.foreground if highlight else (255, 255, 255)
            lowlight_color = lowlight.foreground if lowlight else (128, 128, 128)

            # Draw 3D panel
            renderer.draw_box(19, 2, 4, 78, border_chars, border_fg, border_bg, "3D EFFECTS")

            # Simulated raised button with bevels
            renderer.addstr(20, 4, "Raised:", fg_color, bg_color)

            # Draw raised button at (20, 12) with size 3x10
            btn_y, btn_x = 20, 12
            # Main button area
            renderer.fill_rect(btn_y, btn_x, 1, 10, focused_bg)
            renderer.addstr(btn_y, btn_x, "  [ OK ]  ", focused_fg, focused_bg, bold=True)

            # Highlight (top/left edges)
            for i in range(10):
                renderer.addch(btn_y, btn_x + i, ' ', highlight_color, highlight_color)

            # Draw shadow offset
            for i in range(10):
                renderer.addch(btn_y + 1, btn_x + 2 + i, ' ', shadow_color, shadow_color)

            # Sunken input field
            renderer.addstr(20, 26, "Sunken:", fg_color, bg_color)
            inp_y, inp_x = 20, 34
            renderer.fill_rect(inp_y, inp_x, 1, 16, input_bg)
            renderer.addstr(inp_y, inp_x, "[input field]   ", input_fg, input_bg)

            # Lowlight (top edge for sunken)
            for i in range(16):
                renderer.addch(inp_y, inp_x + i, ' ', lowlight_color, lowlight_color)

            renderer.addstr(21, 4, "Shadows visible on right/bottom edges", fg_color, bg_color)

        except Exception as e:
            # If 3D theme doesn't have all methods, skip 3D panel
            print(f"Warning: Could not render 3D effects for {theme.name}: {e}", file=sys.stderr)

    # Row 23: Footer
    footer = f"Theme: {theme.name} | Colors: RGB | Border: {border_chars[:3]}"
    renderer.addstr(23, 2, footer, fg_color, bg_color)

    return renderer.image


def create_comparison_grid(images: List[Tuple[str, Image.Image]], output_path: str):
    """
    Create a comparison grid showing multiple theme screenshots.

    Args:
        images: List of (theme_name, image) tuples
        output_path: Output file path for the grid image
    """
    if not images:
        return

    # Calculate grid dimensions (aim for roughly square)
    n_images = len(images)
    cols = int(n_images ** 0.5) + 1
    rows = (n_images + cols - 1) // cols

    # Get individual image size
    img_width, img_height = images[0][1].size

    # Create grid image
    grid_width = cols * img_width
    grid_height = rows * img_height
    grid = Image.new('RGB', (grid_width, grid_height), (32, 32, 32))

    # Paste images into grid
    for idx, (name, img) in enumerate(images):
        row = idx // cols
        col = idx % cols
        x = col * img_width
        y = row * img_height
        grid.paste(img, (x, y))

    # Save grid
    grid.save(output_path, 'PNG')
    print(f"Created comparison grid: {output_path}")


def main():
    """Generate screenshots for all registered themes."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate PNG screenshots for all curses-themes"
    )
    parser.add_argument(
        '--output-dir',
        default='screenshots',
        help='Output directory for screenshots (default: screenshots/)'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=80,
        help='Terminal width in characters (default: 80)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=24,
        help='Terminal height in characters (default: 24)'
    )
    parser.add_argument(
        '--font-size',
        type=int,
        default=14,
        help='Font size in points (default: 14)'
    )
    parser.add_argument(
        '--create-grid',
        action='store_true',
        help='Create a comparison grid image'
    )
    parser.add_argument(
        '--theme',
        help='Generate screenshot for a specific theme only'
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating theme screenshots to {output_dir}/")
    print(f"Dimensions: {args.width}x{args.height} characters")
    print(f"Font size: {args.font_size}pt")
    print()

    # Initialize renderer
    renderer = TerminalRenderer(
        width=args.width,
        height=args.height,
        font_size=args.font_size
    )

    # Get themes to render
    all_themes = ThemeManager.list_themes()

    if args.theme:
        # Render single theme
        theme_names = [args.theme]
    else:
        # Render all themes
        theme_names = sorted(all_themes.keys())

    # Track images for comparison grid
    grid_images = []

    # Generate screenshots
    for theme_name in theme_names:
        try:
            print(f"Rendering {theme_name}...", end=' ')

            # Load theme
            theme = ThemeManager.load(theme_name)

            # Render screenshot
            image = render_theme_screenshot(theme, renderer)

            # Save image
            output_file = output_dir / f"{theme_name}.png"
            renderer.save(str(output_file))

            print(f"✓ {output_file}")

            # Add to grid
            if args.create_grid:
                grid_images.append((theme_name, image.copy()))

        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

    print()
    print(f"Generated {len(grid_images)} screenshots")

    # Create comparison grid
    if args.create_grid and grid_images:
        grid_path = output_dir / "comparison.png"
        create_comparison_grid(grid_images, str(grid_path))

    print()
    print("Done!")


if __name__ == '__main__':
    main()
