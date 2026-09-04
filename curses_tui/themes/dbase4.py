#!/usr/bin/env python3
"""
Ashton-Tate/Borland dBASE IV theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# dBASE IV color palette
BLACK = (0, 0, 0)  # #000000
BLUE = (0, 0, 238)  # #0000EE - Control Center blue background
WHITE = (255, 255, 255)  # #FFFFFF
YELLOW = (255, 255, 0)  # #FFFF00 - menu highlighting
CYAN = (0, 255, 255)  # #00FFFF - input fields
RED = (255, 0, 0)  # #FF0000
GREEN = (0, 255, 0)  # #00FF00


class DBase4Theme(Theme):
    """Ashton-Tate/Borland dBASE IV theme with blue Control Center interface."""

    color_map = {
        "background": BLUE,
        "foreground": WHITE,
        "primary": YELLOW,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": YELLOW,
    }

    component_colors = {
        "background": (WHITE, BLUE),
        "button": (YELLOW, BLUE),
        "button_focused": (BLUE, YELLOW),
        "text_input": (CYAN, BLUE),
        "border": (WHITE, BLUE),
        "selection": (BLUE, WHITE),
        "disabled": (BLUE, BLUE),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="dBASE IV",
            description="Ashton-Tate/Borland dBASE IV theme with blue Control Center interface",
            author="FlossWare",
        )
