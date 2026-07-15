#!/usr/bin/env python3
"""
Texas Instruments TI-99/4A home computer theme.

Recreates the distinctive cyan-on-blue aesthetic of the TI-99/4A (1981-1984),
Texas Instruments' entry into the home computer market. The TI-99/4A was notable
for being the first 16-bit home computer and featured the TMS9918A video display
processor with its characteristic color palette.

Historical Context:
    The TI-99/4A competed with the Commodore 64, Apple II, and Atari 8-bit computers.
    Its distinctive cyan text on medium blue background became iconic, particularly in
    the BASIC programming environment and title screens. The cyan-on-blue color scheme
    was warmer and more inviting than the stark white-on-black of many competitors.

Color Scheme:
    - Background: Cyan on blue - the signature TI-99/4A screen appearance
    - Buttons: White on blue - enhanced visibility for interactive elements
    - Focused Elements: Blue on cyan - inverted for clear focus indication
    - Borders: Cyan on blue - consistent with the primary aesthetic
    - Selection: Blue on white - high contrast selection
    - Disabled: Blue on blue - muted appearance

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import ColorPair, Theme


class TI994ATheme(Theme):
    """
    Texas Instruments TI-99/4A home computer theme (1981-1984).

    Recreates the warm cyan-on-blue palette of the first 16-bit home computer.
    Uses ASCII borders for period authenticity (predates widespread Unicode).

    Visual Identity:
        - Primary use of cyan for all text elements
        - White accents for buttons (reflecting the TI's menu systems)
        - Blue-on-white selection (high contrast for CRT displays)
        - ASCII borders for 1981-era authenticity
    """

    # TI-99/4A color palette (approximated in RGB)
    BLACK = (0, 0, 0)  # #000000
    BLUE = (0, 0, 238)  # Medium blue background
    CYAN = (0, 205, 205)  # TI cyan (lighter than pure cyan)
    WHITE = (255, 255, 255)  # #FFFFFF
    GREEN = (0, 205, 0)  # For success messages
    RED = (205, 0, 0)  # For error messages
    YELLOW = (205, 205, 0)  # For warnings

    def __init__(self):
        """Initialize the TI-99/4A theme."""
        super().__init__(
            name="TI-99/4A",
            description="Texas Instruments TI-99/4A home computer theme with cyan-on-blue aesthetic",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: CYAN on BLUE."""
        return ColorPair(self.CYAN, self.BLUE)

    def get_button(self) -> ColorPair:
        """Get button color pair: WHITE on BLUE."""
        return ColorPair(self.WHITE, self.BLUE)

    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair: BLUE on CYAN."""
        return ColorPair(self.BLUE, self.CYAN)

    def get_text_input(self) -> ColorPair:
        """Get text input color pair: CYAN on BLUE."""
        return ColorPair(self.CYAN, self.BLUE)

    def get_border(self) -> ColorPair:
        """Get border color pair: CYAN on BLUE."""
        return ColorPair(self.CYAN, self.BLUE)

    def get_selection(self) -> ColorPair:
        """Get selection color pair: BLUE on WHITE."""
        return ColorPair(self.BLUE, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """Get disabled color pair: BLUE on BLUE (muted)."""
        return ColorPair(self.BLUE, self.BLUE)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters for 1981-era authenticity.

        The TI-99/4A predated widespread Unicode adoption.

        Returns:
            String with 8 ASCII characters for box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the TI-99/4A theme.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: Cyan on blue
            "background": self.BLUE,
            "foreground": self.CYAN,
            # Primary/Button: White on blue (enhanced visibility)
            "primary": self.WHITE,
            # Success: Green on blue
            "success": self.GREEN,
            # Error: Red on blue
            "error": self.RED,
            # Warning: Yellow on blue
            "warning": self.YELLOW,
            # Info: Cyan on blue (matches foreground)
            "info": self.CYAN,
            # Accent: White (matches buttons)
            "accent": self.WHITE,
        }
