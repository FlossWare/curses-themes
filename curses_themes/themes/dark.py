#!/usr/bin/env python3
"""
DarkTheme implementation matching curses-java API.

Dark theme with muted colors and dark background.
Modern dark mode aesthetic.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import ColorPair, Theme


class DarkTheme(Theme):
    """
    Dark theme with muted colors and dark background.
    Modern dark mode aesthetic.

    Matches the curses-java DarkTheme implementation exactly:
    - Background: CYAN on BLACK
    - Button: BLUE on BLACK
    - ButtonFocused: BLACK on BLUE
    - TextInput: WHITE on BLACK
    - Border: BLUE on BLACK
    - Selection: BLACK on CYAN
    - Disabled: BLUE on BLACK (muted)
    - BorderChars: "┌─┐│└─┘│" (Unicode box drawing)
    """

    # Dark theme color values matching Java DarkTheme
    BLACK = (0, 0, 0)  # background
    CYAN = (0, 255, 255)  # foreground, accent
    BLUE = (0, 0, 255)  # primary
    WHITE = (255, 255, 255)  # info
    GREEN = (0, 255, 0)  # success
    YELLOW = (255, 255, 0)  # warning
    RED = (255, 0, 0)  # error

    def __init__(self):
        """Initialize the Dark theme."""
        super().__init__(
            name="Dark",
            description="Dark theme with muted colors and dark background. Modern dark mode aesthetic.",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: CYAN on BLACK."""
        return ColorPair(self.CYAN, self.BLACK)

    def get_button(self) -> ColorPair:
        """Get button color pair: BLUE on BLACK."""
        return ColorPair(self.BLUE, self.BLACK)

    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair: BLACK on BLUE."""
        return ColorPair(self.BLACK, self.BLUE)

    def get_text_input(self) -> ColorPair:
        """Get text input color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_border(self) -> ColorPair:
        """Get border color pair: BLUE on BLACK."""
        return ColorPair(self.BLUE, self.BLACK)

    def get_selection(self) -> ColorPair:
        """Get selection color pair: BLACK on CYAN."""
        return ColorPair(self.BLACK, self.CYAN)

    def get_disabled(self) -> ColorPair:
        """Get disabled color pair: BLUE on BLACK (muted)."""
        return ColorPair(self.BLUE, self.BLACK)

    def get_border_chars(self) -> str:
        """
        Get Unicode border characters.

        Format: top_left, top, top_right, left, right, bottom_left, bottom, bottom_right

        Returns:
            String with 8 characters for Unicode box-drawing: "┌─┐││└─┘"
        """
        return "┌─┐││└─┘"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the Dark theme.

        Maps to exact RGB values matching Java DarkTheme for semantic use.

        Returns:
            Dictionary mapping semantic color names to RGB tuples (0-255)
        """
        return {
            # Background: BLACK (0,0,0)
            "background": self.BLACK,
            # Foreground: CYAN (0,255,255)
            "foreground": self.CYAN,
            # Primary/Button: BLUE (0,0,255) for buttons/borders
            "primary": self.BLUE,
            # Success: GREEN (0,255,0)
            "success": self.GREEN,
            # Error: RED (255,0,0)
            "error": self.RED,
            # Warning: YELLOW (255,255,0)
            "warning": self.YELLOW,
            # Info: WHITE (255,255,255)
            "info": self.WHITE,
            # Accent: CYAN (0,255,255) for selection highlights
            "accent": self.CYAN,
        }
