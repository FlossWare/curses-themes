#!/usr/bin/env python3
"""
Tandy/Radio Shack TRS-80 Model III and Model 4 theme.

Recreates the distinctive white-on-black monochrome display of the TRS-80 Model III
(1980) and Model 4 (1983). These machines featured crisp, high-contrast displays that
made them popular for business applications and word processing.

Historical Context:
    The TRS-80 line was one of the "1977 Trinity" of home computers (along with the
    Apple II and Commodore PET). The Model III improved upon the original Model I with
    an integrated design and cleaner display. The Model 4 added backward compatibility
    and improved graphics capabilities. Both used monochrome displays with exceptional
    clarity - white (or green, depending on the monitor) phosphor on black.

    Radio Shack's business-focused marketing emphasized the professional appearance
    of the monochrome display, contrasting it with the "toy-like" color displays of
    competitors. The crisp white-on-black text was ideal for word processing and
    spreadsheet applications.

Color Scheme:
    - Background: White on black - classic monochrome terminal aesthetic
    - Buttons: White on black - consistent monochrome appearance
    - Focused Elements: Black on white - high-contrast inversion for focus
    - Borders: White on black - crisp boundary definition
    - Selection: Black on white - maximum contrast selection
    - Disabled: Black on black - completely hidden (period-accurate behavior)

Technical Notes:
    The TRS-80 Model III and 4 displayed 64×16 characters (expandable to 80×24 on
    Model 4). The monochrome display was praised for its clarity and lack of color
    fringing, making it superior for text-heavy applications compared to composite
    color monitors of the era.

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

from ..theme import ColorPair, Theme


class TRS80Theme(Theme):
    """
    Tandy/Radio Shack TRS-80 Model III and Model 4 theme (1980-1983).

    Pure monochrome palette with maximum readability. Recreates the professional
    white-on-black display that made the TRS-80 popular for business applications.

    Visual Identity:
        - Pure monochrome palette (white/black only, no color accents)
        - Block-style ASCII borders reflecting character-cell display
        - Sharp contrast ratios optimized for P4 white phosphor CRT monitors
        - Minimalist aesthetic matching Radio Shack's business design philosophy
    """

    # Pure monochrome palette
    BLACK = (0, 0, 0)  # #000000
    WHITE = (255, 255, 255)  # #FFFFFF - P4 white phosphor
    # For semantic colors, we use subtle grays where needed
    LIGHT_GRAY = (192, 192, 192)  # For success/info
    DARK_GRAY = (128, 128, 128)  # For warnings

    def __init__(self):
        """Initialize the TRS-80 theme."""
        super().__init__(
            name="TRS-80",
            description="Tandy/Radio Shack TRS-80 monochrome theme with white-on-black display",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_button(self) -> ColorPair:
        """Get button color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair: BLACK on WHITE (inverted)."""
        return ColorPair(self.BLACK, self.WHITE)

    def get_text_input(self) -> ColorPair:
        """Get text input color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_border(self) -> ColorPair:
        """Get border color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_selection(self) -> ColorPair:
        """Get selection color pair: BLACK on WHITE (maximum contrast)."""
        return ColorPair(self.BLACK, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: BLACK on BLACK (completely hidden).

        Matches the TRS-80's behavior where disabled menu items were
        simply not displayed.
        """
        return ColorPair(self.BLACK, self.BLACK)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters for early 1980s authenticity.

        Uses block-style characters appropriate for the TRS-80's
        character-cell display (1980-1983 era).

        Returns:
            String with 8 ASCII characters for box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the TRS-80 theme.

        Pure monochrome with subtle grays for semantic differentiation.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: White on black
            "background": self.BLACK,
            "foreground": self.WHITE,
            # Primary: White (same as foreground)
            "primary": self.WHITE,
            # Success: Light gray (subtle differentiation)
            "success": self.LIGHT_GRAY,
            # Error: White (no color, but full brightness for visibility)
            "error": self.WHITE,
            # Warning: Dark gray (subtle differentiation)
            "warning": self.DARK_GRAY,
            # Info: White (same as foreground)
            "info": self.WHITE,
            # Accent: White (same as foreground)
            "accent": self.WHITE,
        }
