#!/usr/bin/env python3
"""
Built-in themes for curses applications.

This module provides default theme implementations matching the curses-java library.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from .borland3d import Borland3DTheme
from .dark import DarkTheme
from .dbase3 import DBase3Theme
from .dbase4 import DBase4Theme
from .dbase4_3d import DBase4_3DTheme
from .default import DefaultTheme
from .dos import DOSTheme
from .light import LightTheme
from .ti994a import TI994ATheme
from .trs80 import TRS80Theme

__all__ = [
    "Borland3DTheme",
    "DBase3Theme",
    "DBase4Theme",
    "DBase4_3DTheme",
    "DOSTheme",
    "DarkTheme",
    "DefaultTheme",
    "LightTheme",
    "TI994ATheme",
    "TRS80Theme",
]
