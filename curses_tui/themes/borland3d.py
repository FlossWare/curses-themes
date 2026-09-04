#!/usr/bin/env python3
"""
Borland Turbo Vision 3D theme.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme3d import Theme3D

# Authentic Borland Turbo Vision color palette
# These values match the original CGA/EGA/VGA colors used in Turbo Pascal 6.0+
BLUE = (0, 0, 170)  # #0000AA - The iconic Borland blue background
CYAN = (0, 170, 170)  # #00AAAA - Raised buttons and focus color
YELLOW = (255, 255, 85)  # #FFFF55 - Text on blue (slightly muted for CRT authenticity)
WHITE = (255, 255, 255)  # #FFFFFF - Bright highlights on bevels
BLACK = (0, 0, 0)  # #000000 - Shadows and lowlights
LIGHT_GRAY = (170, 170, 170)  # #AAAAAA - Disabled elements
RED = (255, 85, 85)  # #FF5555 - Error messages
GREEN = (85, 255, 85)  # #55FF55 - Success feedback
MAGENTA = (170, 0, 170)  # #AA00AA - Accent color


class Borland3DTheme(Theme3D):
    """Borland Turbo Vision 3D theme with beveled buttons and drop shadows (1990-1997)."""

    color_map = {
        "background": BLUE,
        "foreground": YELLOW,
        "primary": CYAN,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": CYAN,
        "accent": MAGENTA,
    }

    component_colors = {
        "background": (YELLOW, BLUE),
        "button": (CYAN, BLUE),
        "button_focused": (BLACK, CYAN),
        "text_input": (BLACK, CYAN),
        "border": (CYAN, BLUE),
        "selection": (BLACK, CYAN),
        "disabled": (LIGHT_GRAY, BLUE),
    }

    effects_3d = {
        "shadow": (BLACK, BLACK),
        "highlight": (WHITE, CYAN),
        "lowlight": (BLACK, CYAN),
    }

    border_chars = "╭─╮││╰─╯"
    double_border_chars = "╔═╗║║╚═╝"

    def __init__(self):
        super().__init__(
            name="Borland 3D",
            description="Borland Turbo Vision 3D theme with beveled buttons and drop shadows (1990-1997)",
            author="FlossWare",
        )
        self.shadow_offset_x = 2
        self.shadow_offset_y = 1
