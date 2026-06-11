#!/usr/bin/env python3
"""
Classic MS-DOS and PC-DOS theme.

Recreates the iconic white-on-black text mode interface of MS-DOS and PC-DOS
(1981-1995), the dominant operating system of the PC era. This theme captures
the utilitarian aesthetic of command-line computing that defined an entire
generation of personal computer use.

Historical Context:
    MS-DOS powered the IBM PC and compatibles from 1981 through the mid-1990s.
    Its text-mode interface, typically running in 80×25 character mode with 16 colors,
    became the de facto standard for PC software. The default color scheme was simple:
    white (or light gray) text on a black background, with occasional use of bright
    colors for emphasis.

    Key DOS-era applications like WordPerfect, Lotus 1-2-3, dBASE, and countless
    utilities all shared this visual language. Even early versions of Windows (1.x-3.x)
    were launched from this interface.

Color Scheme:
    - Background: White on black - the standard DOS text mode palette
    - Buttons: Yellow on black - bright color for interactive elements (common in DOS menus)
    - Focused Elements: Black on yellow - inverted for clear visibility
    - Text Input: Cyan on black - distinguishes input fields (common DOS convention)
    - Borders: White on black - simple box-drawing characters
    - Selection: Black on white - high-contrast inverted selection
    - Disabled: Black on black - hidden elements (DOS convention)

Technical Notes:
    DOS text mode used the IBM PC's 16-color palette derived from CGA (1981).
    The 8 base colors could be displayed in normal or bright (high-intensity) variants.
    This theme maps to the standard 8-color ncurses palette while maintaining the
    DOS aesthetic through careful color selection.

    The ASCII box-drawing characters used here (+-+||+-+) are simplified versions
    of the IBM extended ASCII characters (═║╔╗╚╝) that were standard in DOS applications.
    For maximum compatibility, we use the simpler ASCII set.

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


class DOSTheme(Theme):
    """
    Classic MS-DOS and PC-DOS theme (1981-1995).

    Recreates the utilitarian white-on-black interface with strategic use of
    yellow for menus and cyan for input fields.

    Visual Identity:
        - Strategic use of yellow for interactive elements (DOS menu conventions)
        - Cyan text input fields (common DOS application pattern)
        - ASCII box-drawing characters (IBM extended ASCII, code page 437)
        - High-contrast color choices optimized for CGA/EGA/VGA displays
    """

    # DOS CGA/EGA/VGA color palette (standard PC colors)
    BLACK = (0, 0, 0)  # #000000
    WHITE = (255, 255, 255)  # #FFFFFF (bright white)
    YELLOW = (255, 255, 0)  # #FFFF00 (bright yellow)
    CYAN = (0, 255, 255)  # #00FFFF (bright cyan)
    RED = (255, 0, 0)  # #FF0000 (bright red)
    GREEN = (0, 255, 0)  # #00FF00 (bright green)
    MAGENTA = (255, 0, 255)  # #FF00FF (bright magenta)

    def __init__(self):
        """Initialize the DOS theme."""
        super().__init__(
            name="DOS",
            description="Classic MS-DOS and PC-DOS theme with white-on-black text mode interface",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_button(self) -> ColorPair:
        """
        Get button color pair: YELLOW on BLACK.

        Bright color for menu items and buttons, a common DOS convention
        for highlighting interactive elements.
        """
        return ColorPair(self.YELLOW, self.BLACK)

    def get_button_focused(self) -> ColorPair:
        """
        Get focused button color pair: BLACK on YELLOW.

        Inverted colors for clear focus indication, matching the DOS
        convention for selected menu items.
        """
        return ColorPair(self.BLACK, self.YELLOW)

    def get_text_input(self) -> ColorPair:
        """
        Get text input color pair: CYAN on BLACK.

        Distinguishes input fields from regular text, a common pattern in
        DOS applications for form fields and user input areas.
        """
        return ColorPair(self.CYAN, self.BLACK)

    def get_border(self) -> ColorPair:
        """Get border color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_selection(self) -> ColorPair:
        """
        Get selection color pair: BLACK on WHITE.

        Maximum contrast selection, matching DOS's inverted selection highlighting.
        """
        return ColorPair(self.BLACK, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: BLACK on BLACK.

        Invisible disabled items, matching DOS behavior where unavailable
        menu items were typically hidden rather than grayed out.
        """
        return ColorPair(self.BLACK, self.BLACK)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters for universal compatibility.

        In authentic DOS, these would be the IBM extended ASCII box-drawing
        characters from code page 437 (═║╔╗╚╝).

        Returns:
            String with 8 ASCII characters for box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the DOS theme.

        Uses the standard CGA/EGA/VGA 16-color palette.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: White on black
            "background": self.BLACK,
            "foreground": self.WHITE,
            # Primary/Button: Yellow on black (DOS menu highlight)
            "primary": self.YELLOW,
            # Success: Green on black
            "success": self.GREEN,
            # Error: Red on black
            "error": self.RED,
            # Warning: Yellow on black (same as primary)
            "warning": self.YELLOW,
            # Info: Cyan on black (matches text input)
            "info": self.CYAN,
            # Accent: Magenta on black (for special highlights)
            "accent": self.MAGENTA,
        }
