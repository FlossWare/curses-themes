#!/usr/bin/env python3
"""
Classic MS-DOS and PC-DOS theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# DOS CGA/EGA/VGA color palette (standard PC colors)
BLACK = (0, 0, 0)  # #000000
WHITE = (255, 255, 255)  # #FFFFFF (bright white)
YELLOW = (255, 255, 0)  # #FFFF00 (bright yellow)
CYAN = (0, 255, 255)  # #00FFFF (bright cyan)
RED = (255, 0, 0)  # #FF0000 (bright red)
GREEN = (0, 255, 0)  # #00FF00 (bright green)
MAGENTA = (255, 0, 255)  # #FF00FF (bright magenta)


class DOSTheme(Theme):
    """Classic MS-DOS and PC-DOS theme with white-on-black text mode interface."""

    color_map = {
        "background": BLACK,
        "foreground": WHITE,
        "primary": YELLOW,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": MAGENTA,
    }

    component_colors = {
        "background": (WHITE, BLACK),
        "button": (YELLOW, BLACK),
        "button_focused": (BLACK, YELLOW),
        "text_input": (CYAN, BLACK),
        "border": (WHITE, BLACK),
        "selection": (BLACK, WHITE),
        "disabled": (BLACK, BLACK),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="DOS",
            description="Classic MS-DOS and PC-DOS theme with white-on-black text mode interface",
            author="FlossWare",
        )
