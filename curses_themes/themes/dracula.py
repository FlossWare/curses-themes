#!/usr/bin/env python3
"""
Dracula theme — official Dracula color palette for terminal UIs.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Official Dracula palette (https://draculatheme.com/spec)
BACKGROUND = (40, 42, 54)  # #282A36
FOREGROUND = (248, 248, 242)  # #F8F8F2
CURRENT_LINE = (68, 71, 90)  # #44475A
COMMENT = (98, 114, 164)  # #6272A4
CYAN = (139, 233, 253)  # #8BE9FD
GREEN = (80, 250, 123)  # #50FA7B
ORANGE = (255, 184, 108)  # #FFB86C
PINK = (255, 121, 198)  # #FF79C6
PURPLE = (189, 147, 249)  # #BD93F9
RED = (255, 85, 85)  # #FF5555
YELLOW = (241, 250, 140)  # #F1FA8C


class DraculaTheme(Theme):
    """Dracula theme with the official dark palette — popular among developers."""

    color_map = {
        "background": BACKGROUND,
        "foreground": FOREGROUND,
        "primary": PURPLE,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": PINK,
    }

    component_colors = {
        "background": (FOREGROUND, BACKGROUND),
        "button": (PURPLE, BACKGROUND),
        "button_focused": (BACKGROUND, PURPLE),
        "text_input": (FOREGROUND, CURRENT_LINE),
        "border": (COMMENT, BACKGROUND),
        "selection": (FOREGROUND, CURRENT_LINE),
        "disabled": (COMMENT, BACKGROUND),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Dracula",
            description=(
                "Official Dracula dark theme with purple accents. "
                "Popular modern developer palette."
            ),
            author="FlossWare (palette by Zeno Rocha)",
        )
