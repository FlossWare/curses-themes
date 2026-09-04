#!/usr/bin/env python3
"""
Ashton-Tate dBASE III and dBASE III Plus theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# dBASE III color palette
BLACK = (0, 0, 0)  # #000000
WHITE = (255, 255, 255)  # #FFFFFF
CYAN = (0, 255, 255)  # #00FFFF - dBASE's signature menu color
GREEN = (0, 255, 0)  # #00FF00 - for data entry fields
RED = (255, 0, 0)  # #FF0000
YELLOW = (255, 255, 0)  # #FFFF00


class DBase3Theme(Theme):
    """Ashton-Tate dBASE III and dBASE III Plus theme with cyan menus on black background."""

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
        "selection": (BLACK, CYAN),
        "disabled": (BLACK, BLACK),
    }

    border_chars = "+-+||+-+"

    def __init__(self):
        super().__init__(
            name="dBASE III",
            description="Ashton-Tate dBASE III theme with cyan menus on black background",
            author="FlossWare",
        )
