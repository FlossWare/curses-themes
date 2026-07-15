#!/usr/bin/env python3
"""
Tandy/Radio Shack TRS-80 Model III and Model 4 theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Pure monochrome palette
BLACK = (0, 0, 0)  # #000000
WHITE = (255, 255, 255)  # #FFFFFF - P4 white phosphor
# For semantic colors, we use subtle grays where needed
LIGHT_GRAY = (192, 192, 192)  # For success/info
DARK_GRAY = (128, 128, 128)  # For warnings


class TRS80Theme(Theme):
    """Tandy/Radio Shack TRS-80 monochrome theme with white-on-black display."""

    color_map = {
        "background": BLACK,
        "foreground": WHITE,
        "primary": WHITE,
        "success": LIGHT_GRAY,
        "error": WHITE,
        "warning": DARK_GRAY,
        "info": WHITE,
        "accent": WHITE,
    }

    component_colors = {
        "background": (WHITE, BLACK),
        "button": (WHITE, BLACK),
        "button_focused": (BLACK, WHITE),
        "text_input": (WHITE, BLACK),
        "border": (WHITE, BLACK),
        "selection": (BLACK, WHITE),
        "disabled": (BLACK, BLACK),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="TRS-80",
            description="Tandy/Radio Shack TRS-80 monochrome theme with white-on-black display",
            author="FlossWare",
        )
