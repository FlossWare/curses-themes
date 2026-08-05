#!/usr/bin/env python3
"""
Built-in themes for curses applications.

This module provides default theme implementations matching the curses-java library
plus popular modern developer palettes.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from .borland3d import Borland3DTheme
from .catppuccin import CatppuccinTheme
from .dark import DarkTheme
from .dbase3 import DBase3Theme
from .dbase4 import DBase4Theme
from .dbase4_3d import DBase4_3DTheme
from .default import DefaultTheme
from .dos import DOSTheme
from .dracula import DraculaTheme
from .light import LightTheme
from .monokai import MonokaiTheme
from .nord import NordTheme
from .solarized_dark import SolarizedDarkTheme
from .solarized_light import SolarizedLightTheme
from .ti994a import TI994ATheme
from .trs80 import TRS80Theme

__all__ = [
    "Borland3DTheme",
    "CatppuccinTheme",
    "DBase3Theme",
    "DBase4Theme",
    "DBase4_3DTheme",
    "DOSTheme",
    "DarkTheme",
    "DefaultTheme",
    "DraculaTheme",
    "LightTheme",
    "MonokaiTheme",
    "NordTheme",
    "SolarizedDarkTheme",
    "SolarizedLightTheme",
    "TI994ATheme",
    "TRS80Theme",
]
