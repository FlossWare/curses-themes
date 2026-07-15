#!/usr/bin/env python3
"""
Texas Instruments TI-99/4A home computer theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# TI-99/4A color palette (approximated in RGB)
BLACK = (0, 0, 0)  # #000000
BLUE = (0, 0, 238)  # Medium blue background
CYAN = (0, 205, 205)  # TI cyan (lighter than pure cyan)
WHITE = (255, 255, 255)  # #FFFFFF
GREEN = (0, 205, 0)  # For success messages
RED = (205, 0, 0)  # For error messages
YELLOW = (205, 205, 0)  # For warnings


class TI994ATheme(Theme):
    """Texas Instruments TI-99/4A home computer theme with cyan-on-blue aesthetic."""

    color_map = {
        "background": BLUE,
        "foreground": CYAN,
        "primary": WHITE,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": WHITE,
    }

    component_colors = {
        "background": (CYAN, BLUE),
        "button": (WHITE, BLUE),
        "button_focused": (BLUE, CYAN),
        "text_input": (CYAN, BLUE),
        "border": (CYAN, BLUE),
        "selection": (BLUE, WHITE),
        "disabled": (BLUE, BLUE),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="TI-99/4A",
            description="Texas Instruments TI-99/4A home computer theme with cyan-on-blue aesthetic",
            author="FlossWare",
        )
