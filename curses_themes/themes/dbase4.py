#!/usr/bin/env python3
"""
Ashton-Tate/Borland dBASE IV theme.

Recreates the more sophisticated windowed interface of dBASE IV (1988-1993),
which introduced a revolutionary menu-driven interface with multiple windows,
pull-down menus, and mouse support. This was a significant departure from
dBASE III's command-line focus.

Historical Context:
    dBASE IV was released in 1988 with great fanfare, introducing a graphical
    menu system (the Control Center) that replaced the traditional dot prompt as
    the default interface. The new interface used a blue background with white and
    yellow text, creating a more modern and accessible appearance.

    Despite initial bugs that hurt its reputation, dBASE IV eventually became
    stable and was acquired by Borland in 1991. Its windowed interface and menu
    system influenced database tools throughout the 1990s. The Control Center's
    blue-and-white color scheme became iconic.

Color Scheme:
    - Background: White on blue - the Control Center's main interface
    - Buttons/Menus: Yellow on blue - menu bar and highlighted options
    - Focused Elements: Blue on yellow - inverted menu selection
    - Text Input: Cyan on blue - data entry fields in forms
    - Borders: White on blue - window frames and separators
    - Selection: Blue on white - highlighted records in browse mode
    - Disabled: Blue on blue - dimmed unavailable options

Technical Notes:
    dBASE IV required EGA or better graphics (VGA recommended) and took advantage
    of the expanded color palette. The Control Center interface ran in 80×25 or
    80×43/50 text modes, using box-drawing characters for window frames and menus.

    The shift from black to blue backgrounds was part of a broader trend in
    late-1980s software design, also seen in Lotus 1-2-3 Release 3 and other
    applications moving toward GUI-inspired interfaces.

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

from ..theme import ColorPair, Theme


class DBase4Theme(Theme):
    """
    Ashton-Tate/Borland dBASE IV theme (1988-1993).

    Recreates the modernized blue-background Control Center interface that
    represented the evolution from command-line to GUI-inspired database tools.

    Visual Identity:
        - Blue background (versus dBASE III's black) for a softer, professional look
        - Yellow menu highlighting (departure from cyan) for better visibility
        - White borders and text matching the Control Center windows
        - Cyan input fields distinguishing data entry from display text
    """

    # dBASE IV color palette
    BLACK = (0, 0, 0)  # #000000
    BLUE = (0, 0, 238)  # #0000EE - Control Center blue background
    WHITE = (255, 255, 255)  # #FFFFFF
    YELLOW = (255, 255, 0)  # #FFFF00 - menu highlighting
    CYAN = (0, 255, 255)  # #00FFFF - input fields
    RED = (255, 0, 0)  # #FF0000
    GREEN = (0, 255, 0)  # #00FF00

    def __init__(self):
        """Initialize the dBASE IV theme."""
        super().__init__(
            name="dBASE IV",
            description="Ashton-Tate/Borland dBASE IV theme with blue Control Center interface",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """
        Get background color pair: WHITE on BLUE.

        The Control Center's main interface color scheme.
        """
        return ColorPair(self.WHITE, self.BLUE)

    def get_button(self) -> ColorPair:
        """
        Get button color pair: YELLOW on BLUE.

        Menu bar and menu items in the iconic dBASE IV yellow.
        """
        return ColorPair(self.YELLOW, self.BLUE)

    def get_button_focused(self) -> ColorPair:
        """
        Get focused button color pair: BLUE on YELLOW.

        Inverted menu selection for clear focus indication.
        """
        return ColorPair(self.BLUE, self.YELLOW)

    def get_text_input(self) -> ColorPair:
        """
        Get text input color pair: CYAN on BLUE.

        Data entry fields in forms and dialogs, distinguishing input
        from display-only text.
        """
        return ColorPair(self.CYAN, self.BLUE)

    def get_border(self) -> ColorPair:
        """
        Get border color pair: WHITE on BLUE.

        Window frames and separators in the Control Center.
        """
        return ColorPair(self.WHITE, self.BLUE)

    def get_selection(self) -> ColorPair:
        """
        Get selection color pair: BLUE on WHITE.

        Highlighted records in browse mode and selected items.
        """
        return ColorPair(self.BLUE, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: BLUE on BLUE.

        Dimmed unavailable menu items (subtle muting effect).
        """
        return ColorPair(self.BLUE, self.BLUE)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters for maximum compatibility.

        In authentic dBASE IV, these would be extended ASCII double-line boxes.

        Returns:
            String with 8 ASCII characters for box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the dBASE IV theme.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: White on blue (Control Center)
            "background": self.BLUE,
            "foreground": self.WHITE,
            # Primary/Button: Yellow on blue (menu highlighting)
            "primary": self.YELLOW,
            # Success: Green on blue
            "success": self.GREEN,
            # Error: Red on blue
            "error": self.RED,
            # Warning: Yellow on blue (same as primary)
            "warning": self.YELLOW,
            # Info: Cyan on blue (matches text input)
            "info": self.CYAN,
            # Accent: Yellow (matches buttons/menus)
            "accent": self.YELLOW,
        }
