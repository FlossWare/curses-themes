#!/usr/bin/env python3
"""
Monokai theme — classic Sublime Text / TextMate inspired palette.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Classic Monokai palette
BACKGROUND = (39, 40, 34)  # #272822
FOREGROUND = (248, 248, 242)  # #F8F8F2
COMMENT = (117, 113, 94)  # #75715E
RED = (249, 38, 114)  # #F92672
ORANGE = (253, 151, 31)  # #FD971F
YELLOW = (230, 219, 116)  # #E6DB74
GREEN = (166, 226, 46)  # #A6E22E
CYAN = (102, 217, 239)  # #66D9EF
PURPLE = (174, 129, 255)  # #AE81FF
SELECTION = (73, 72, 62)  # #49483E


class MonokaiTheme(Theme):
    """Monokai — vibrant classic editor palette popular since TextMate/Sublime."""

    color_map = {
        "background": BACKGROUND,
        "foreground": FOREGROUND,
        "primary": CYAN,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": PURPLE,
    }

    component_colors = {
        "background": (FOREGROUND, BACKGROUND),
        "button": (CYAN, BACKGROUND),
        "button_focused": (BACKGROUND, CYAN),
        "text_input": (FOREGROUND, SELECTION),
        "border": (COMMENT, BACKGROUND),
        "selection": (FOREGROUND, SELECTION),
        "disabled": (COMMENT, BACKGROUND),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Monokai",
            description=(
                "Classic Monokai palette from TextMate/Sublime Text. "
                "Vibrant colors on a warm dark background."
            ),
            author="FlossWare (palette inspired by Wimer Hazenberg)",
        )
