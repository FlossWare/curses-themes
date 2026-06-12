#!/usr/bin/env python3
"""
LightTheme implementation matching curses-java API.

Light theme with bright background and dark text.
Clean, high-contrast light mode aesthetic.

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


class LightTheme(Theme):
    """
    Light theme with bright background and dark text.
    Clean, high-contrast light mode aesthetic.

    Matches the curses-java LightTheme implementation exactly:
    - Background: BLACK on WHITE
    - Button: BLUE on WHITE
    - ButtonFocused: WHITE on BLUE
    - TextInput: BLACK on CYAN
    - Border: BLACK on WHITE
    - Selection: WHITE on BLUE
    - Disabled: CYAN on WHITE
    - BorderChars: "╔═╗║╚═╝║" (Unicode double-line box drawing)
    """

    # Color definitions matching the specification
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 128, 0)
    ORANGE = (255, 165, 0)
    RED = (255, 0, 0)

    def __init__(self):
        """Initialize the Light theme."""
        super().__init__(
            name="Light",
            description="Light theme with bright background and dark text. Clean, high-contrast light mode aesthetic.",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: BLACK on WHITE."""
        return ColorPair(self.BLACK, self.WHITE)

    def get_button(self) -> ColorPair:
        """Get button color pair: BLUE on WHITE."""
        return ColorPair(self.BLUE, self.WHITE)

    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair: WHITE on BLUE."""
        return ColorPair(self.WHITE, self.BLUE)

    def get_text_input(self) -> ColorPair:
        """Get text input color pair: BLACK on CYAN."""
        return ColorPair(self.BLACK, self.CYAN)

    def get_border(self) -> ColorPair:
        """Get border color pair: BLACK on WHITE."""
        return ColorPair(self.BLACK, self.WHITE)

    def get_selection(self) -> ColorPair:
        """Get selection color pair: WHITE on BLUE."""
        return ColorPair(self.WHITE, self.BLUE)

    def get_disabled(self) -> ColorPair:
        """Get disabled color pair: CYAN on WHITE."""
        return ColorPair(self.CYAN, self.WHITE)

    def get_border_chars(self) -> str:
        """
        Get double-line Unicode border characters.

        Format: top_left, top, top_right, left, right, bottom_left, bottom, bottom_right

        Returns:
            String with 8 characters for double-line Unicode box-drawing: "╔═╗║║╚═╝"
        """
        return "╔═╗║║╚═╝"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the Light theme.

        Maps to ncurses standard colors for semantic use.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: BLACK on WHITE
            "background": self.WHITE,
            "foreground": self.BLACK,
            # Primary/Button: BLUE on WHITE
            "primary": self.BLUE,
            # Success: GREEN
            "success": self.GREEN,
            # Error: RED
            "error": self.RED,
            # Warning: ORANGE
            "warning": self.ORANGE,
            # Accent: CYAN
            "accent": self.CYAN,
            # Info: BLUE (matches primary)
            "info": self.BLUE,
        }
