#!/usr/bin/env python3
"""
Default theme with white text on black background.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Standard 256-color terminal values (0-255 RGB)
BLACK = (0, 0, 0)  # #000000
WHITE = (255, 255, 255)  # #FFFFFF
CYAN = (0, 255, 255)  # #00FFFF
GREEN = (0, 255, 0)  # #00FF00
RED = (255, 0, 0)  # #FF0000
YELLOW = (255, 255, 0)  # #FFFF00


class DefaultTheme(Theme):
    """Default theme matching curses-java DefaultTheme with classic terminal appearance."""

    color_map = {
        "background": BLACK,
        "foreground": WHITE,
        "primary": CYAN,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": CYAN,
    }

    component_colors = {
        "background": (WHITE, BLACK),
        "button": (CYAN, BLACK),
        "button_focused": (BLACK, CYAN),
        "text_input": (GREEN, BLACK),
        "border": (WHITE, BLACK),
        "selection": (BLACK, WHITE),
        "disabled": (WHITE, BLACK),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="Default",
            description="Default theme with white text on black background. Classic terminal appearance.",
            author="FlossWare",
        )
