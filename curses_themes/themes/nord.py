#!/usr/bin/env python3
"""
Nord theme — Arctic, north-bluish color palette.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Official Nord palette (https://www.nordtheme.com/)
# Polar Night
NORD0 = (46, 52, 64)  # #2E3440
NORD1 = (59, 66, 82)  # #3B4252
NORD2 = (67, 76, 94)  # #434C5E
NORD3 = (76, 86, 106)  # #4C566A
# Snow Storm
NORD4 = (216, 222, 233)  # #D8DEE9
NORD5 = (229, 233, 240)  # #E5E9F0
NORD6 = (236, 239, 244)  # #ECEFF4
# Frost
NORD7 = (143, 188, 187)  # #8FBCBB
NORD8 = (136, 192, 208)  # #88C0D0
NORD9 = (129, 161, 193)  # #81A1C1
NORD10 = (94, 129, 172)  # #5E81AC
# Aurora
NORD11 = (191, 97, 106)  # #BF616A
NORD12 = (208, 135, 112)  # #D08770
NORD13 = (235, 203, 139)  # #EBCB8B
NORD14 = (163, 190, 140)  # #A3BE8C
NORD15 = (180, 142, 173)  # #B48EAD


class NordTheme(Theme):
    """Nord theme — arctic, north-bluish color palette for calm terminal UIs."""

    color_map = {
        "background": NORD0,
        "foreground": NORD4,
        "primary": NORD8,
        "success": NORD14,
        "error": NORD11,
        "warning": NORD13,
        "info": NORD9,
        "accent": NORD15,
    }

    component_colors = {
        "background": (NORD4, NORD0),
        "button": (NORD8, NORD1),
        "button_focused": (NORD0, NORD8),
        "text_input": (NORD4, NORD1),
        "border": (NORD3, NORD0),
        "selection": (NORD6, NORD2),
        "disabled": (NORD3, NORD0),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Nord",
            description=(
                "Arctic, north-bluish color palette. "
                "Calm and elegant dark theme."
            ),
            author="FlossWare (palette by Arctic Ice Studio)",
        )
