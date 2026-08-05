#!/usr/bin/env python3
"""
Solarized Dark theme — precision colors by Ethan Schoonover.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Official Solarized palette (https://ethanschoonover.com/solarized/)
BASE03 = (0, 43, 54)  # #002B36
BASE02 = (7, 54, 66)  # #073642
BASE01 = (88, 110, 117)  # #586E75
BASE00 = (101, 123, 131)  # #657B83
BASE0 = (131, 148, 150)  # #839496
BASE1 = (147, 161, 161)  # #93A1A1
BASE2 = (238, 232, 213)  # #EEE8D5
BASE3 = (253, 246, 227)  # #FDF6E3
YELLOW = (181, 137, 0)  # #B58900
ORANGE = (203, 75, 22)  # #CB4B16
RED = (220, 50, 47)  # #DC322F
MAGENTA = (211, 54, 130)  # #D33682
VIOLET = (108, 113, 196)  # #6C71C4
BLUE = (38, 139, 210)  # #268BD2
CYAN = (42, 161, 152)  # #2AA198
GREEN = (133, 153, 0)  # #859900


class SolarizedDarkTheme(Theme):
    """Solarized Dark — precision colors for machines and people."""

    color_map = {
        "background": BASE03,
        "foreground": BASE0,
        "primary": BLUE,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": MAGENTA,
    }

    component_colors = {
        "background": (BASE0, BASE03),
        "button": (BLUE, BASE02),
        "button_focused": (BASE03, BLUE),
        "text_input": (BASE1, BASE02),
        "border": (BASE01, BASE03),
        "selection": (BASE3, BASE02),
        "disabled": (BASE01, BASE03),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Solarized Dark",
            description=(
                "Solarized Dark palette by Ethan Schoonover. "
                "Precision colors optimized for readability."
            ),
            author="FlossWare (palette by Ethan Schoonover)",
        )
