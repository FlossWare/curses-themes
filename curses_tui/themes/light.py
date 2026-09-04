#!/usr/bin/env python3
"""
LightTheme implementation matching curses-java API.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Color definitions matching the specification
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 128, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)


class LightTheme(Theme):
    """Light theme with bright background and dark text. Clean, high-contrast light mode aesthetic."""

    color_map = {
        "background": WHITE,
        "foreground": BLACK,
        "primary": BLUE,
        "success": GREEN,
        "error": RED,
        "warning": ORANGE,
        "info": BLUE,
        "accent": CYAN,
    }

    component_colors = {
        "background": (BLACK, WHITE),
        "button": (BLUE, WHITE),
        "button_focused": (WHITE, BLUE),
        "text_input": (BLACK, CYAN),
        "border": (BLACK, WHITE),
        "selection": (WHITE, BLUE),
        "disabled": (CYAN, WHITE),
    }

    border_chars = "╔═╗║║╚═╝"

    def __init__(self):
        super().__init__(
            name="Light",
            description="Light theme with bright background and dark text. Clean, high-contrast light mode aesthetic.",
            author="FlossWare",
        )
