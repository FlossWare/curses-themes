#!/usr/bin/env python3
"""
Catppuccin Mocha theme — soothin' pastel dark palette.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Catppuccin Mocha palette (https://github.com/catppuccin/catppuccin)
BASE = (30, 30, 46)  # #1E1E2E
MANTLE = (24, 24, 37)  # #181825
CRUST = (17, 17, 27)  # #11111B
TEXT = (205, 214, 244)  # #CDD6F4
SUBTEXT1 = (186, 194, 222)  # #BAC2DE
SUBTEXT0 = (166, 173, 200)  # #A6ADC8
OVERLAY2 = (147, 153, 178)  # #9399B2
OVERLAY1 = (127, 132, 156)  # #7F849C
OVERLAY0 = (108, 112, 134)  # #6C7086
SURFACE2 = (88, 91, 112)  # #585B70
SURFACE1 = (69, 71, 90)  # #45475A
SURFACE0 = (49, 50, 68)  # #313244
ROSEWATER = (245, 224, 220)  # #F5E0DC
FLAMINGO = (242, 205, 205)  # #F2CDCD
PINK = (245, 194, 231)  # #F5C2E7
MAUVE = (203, 166, 247)  # #CBA6F7
RED = (243, 139, 168)  # #F38BA8
MAROON = (235, 160, 172)  # #EBA0AC
PEACH = (250, 179, 135)  # #FAB387
YELLOW = (249, 226, 175)  # #F9E2AF
GREEN = (166, 227, 161)  # #A6E3A1
TEAL = (148, 226, 213)  # #94E2D5
SKY = (137, 220, 235)  # #89DCEB
SAPPHIRE = (116, 199, 236)  # #74C7EC
BLUE = (137, 180, 250)  # #89B4FA
LAVENDER = (180, 190, 254)  # #B4BEFE


class CatppuccinTheme(Theme):
    """Catppuccin Mocha — soothin' pastel dark palette for modern TUIs."""

    color_map = {
        "background": BASE,
        "foreground": TEXT,
        "primary": BLUE,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": SKY,
        "accent": MAUVE,
    }

    component_colors = {
        "background": (TEXT, BASE),
        "button": (BLUE, SURFACE0),
        "button_focused": (BASE, BLUE),
        "text_input": (TEXT, SURFACE0),
        "border": (OVERLAY0, BASE),
        "selection": (TEXT, SURFACE1),
        "disabled": (OVERLAY0, BASE),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Catppuccin",
            description=(
                "Catppuccin Mocha pastel dark theme. "
                "Soft, soothin' colors for modern terminal UIs."
            ),
            author="FlossWare (palette by Catppuccin community)",
        )
