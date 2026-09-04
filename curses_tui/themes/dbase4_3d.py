#!/usr/bin/env python3
"""
Ashton-Tate/Borland dBASE IV 3D windowed interface theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme3d import Theme3D

# dBASE IV 3D color palette
BLACK = (0, 0, 0)  # #000000 - shadows and lowlights
BLUE = (0, 0, 238)  # #0000EE - Control Center blue background
WHITE = (255, 255, 255)  # #FFFFFF - highlights and borders
YELLOW = (255, 255, 0)  # #FFFF00 - raised menu buttons
CYAN = (0, 255, 255)  # #00FFFF - sunken input fields
RED = (255, 0, 0)  # #FF0000 - error messages
GREEN = (0, 255, 0)  # #00FF00 - success indicators


class DBase4_3DTheme(Theme3D):
    """Ashton-Tate/Borland dBASE IV 3D windowed Control Center with drop shadows and beveled frames."""

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

    effects_3d = {
        "shadow": (BLACK, BLACK),
        "highlight": (WHITE, WHITE),
        "lowlight": (BLACK, BLUE),
    }

    border_chars = "┌─┐││└─┘"
    double_border_chars = "╔═╗║║╚═╝"

    def __init__(self):
        super().__init__(
            name="dBASE IV 3D",
            description="Ashton-Tate/Borland dBASE IV 3D windowed Control Center with drop shadows and beveled frames",
            author="FlossWare",
        )
        self.shadow_offset_x = 2
        self.shadow_offset_y = 1
