#!/usr/bin/env python3
"""
Built-in themes for curses applications.

This module provides default theme implementations matching the curses-java library.

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .default import DefaultTheme
from .dark import DarkTheme
from .light import LightTheme
from .ti994a import TI994ATheme
from .trs80 import TRS80Theme
from .dos import DOSTheme
from .dbase3 import DBase3Theme
from .dbase4 import DBase4Theme
from .borland3d import Borland3DTheme
from .dbase4_3d import DBase4_3DTheme

__all__ = [
    'DefaultTheme',
    'DarkTheme',
    'LightTheme',
    'TI994ATheme',
    'TRS80Theme',
    'DOSTheme',
    'DBase3Theme',
    'DBase4Theme',
    'Borland3DTheme',
    'DBase4_3DTheme',
]
