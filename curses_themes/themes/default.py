#!/usr/bin/env python3
"""
Default theme with white text on black background.

Matches the curses-java DefaultTheme with classic terminal appearance.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import ColorPair, Theme


class DefaultTheme(Theme):
    """
    Default theme matching curses-java DefaultTheme.

    Color scheme:
    - Background: WHITE on BLACK
    - Button: CYAN on BLACK
    - ButtonFocused: BLACK on CYAN
    - TextInput: GREEN on BLACK
    - Border: WHITE on BLACK
    - Selection: BLACK on WHITE
    - Disabled: WHITE on BLACK (dimmed)
    - BorderChars: "+-+||+-+" (ASCII)

    This theme provides a classic terminal appearance with white text on
    a black background, suitable for most terminal environments.
    """

    # Standard 256-color terminal values (0-255 RGB)
    BLACK = (0, 0, 0)  # #000000
    WHITE = (255, 255, 255)  # #FFFFFF
    CYAN = (0, 255, 255)  # #00FFFF
    GREEN = (0, 255, 0)  # #00FF00
    RED = (255, 0, 0)  # #FF0000
    YELLOW = (255, 255, 0)  # #FFFF00

    def __init__(self):
        """Initialize the Default theme."""
        super().__init__(
            name="Default",
            description="Default theme with white text on black background. Classic terminal appearance.",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """Get background color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_button(self) -> ColorPair:
        """Get button color pair: CYAN on BLACK."""
        return ColorPair(self.CYAN, self.BLACK)

    def get_button_focused(self) -> ColorPair:
        """Get focused button color pair: BLACK on CYAN."""
        return ColorPair(self.BLACK, self.CYAN)

    def get_text_input(self) -> ColorPair:
        """Get text input color pair: GREEN on BLACK."""
        return ColorPair(self.GREEN, self.BLACK)

    def get_border(self) -> ColorPair:
        """Get border color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_selection(self) -> ColorPair:
        """Get selection color pair: BLACK on WHITE."""
        return ColorPair(self.BLACK, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """Get disabled color pair: WHITE on BLACK (dimmed)."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters.

        Matches Java BorderChars: "+-+||+-+"
        Format: top_left, top, top_right, left, right, bottom_left, bottom, bottom_right

        Returns:
            String with 8 characters for ASCII box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the Default theme.

        Maps to ncurses standard colors for semantic use.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: WHITE on BLACK
            "background": self.BLACK,
            "foreground": self.WHITE,
            # Primary/Button: CYAN on BLACK (maps to button and focused states)
            "primary": self.CYAN,
            # Success/TextInput: GREEN on BLACK
            "success": self.GREEN,
            # Error: RED on BLACK
            "error": self.RED,
            # Warning: YELLOW on BLACK
            "warning": self.YELLOW,
            # Info: CYAN on BLACK (same as primary)
            "info": self.CYAN,
            # Accent/Selection: Uses inverse (BLACK on WHITE handled by component)
            "accent": self.CYAN,
        }
