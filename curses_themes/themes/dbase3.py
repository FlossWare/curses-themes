#!/usr/bin/env python3
"""
Ashton-Tate dBASE III and dBASE III Plus theme.

Recreates the utilitarian interface of dBASE III (1984) and dBASE III Plus (1985),
the database management system that dominated the PC database market in the mid-1980s.
dBASE III's command-line "dot prompt" and simple menu system became the standard
interface pattern for business database applications.

Historical Context:
    dBASE III revolutionized database management on personal computers, bringing
    mainframe-style database capabilities to the IBM PC. Its distinctive interface
    featured a black background with white text for the command line, and cyan text
    for menus and prompts. The program's ".dbf" file format became an industry standard,
    still used today.

    By 1985, dBASE III Plus had become the best-selling database software, powering
    thousands of custom business applications. Its programming language (xBase) spawned
    numerous clones including Clipper, FoxPro, and others.

Color Scheme:
    - Background: White on black - the classic dot prompt interface
    - Buttons/Menus: Cyan on black - distinctive menu highlighting
    - Focused Elements: Black on cyan - inverted selection
    - Text Input: Green on black - data entry fields (common in dBASE apps)
    - Borders: White on black - simple box drawing
    - Selection: Black on cyan - highlighted database records
    - Disabled: Black on black - hidden unavailable options

Technical Notes:
    dBASE III ran in DOS text mode (80×25) and used the standard CGA/EGA color
    palette. The cyan-on-black color scheme was chosen for its high readability on
    composite monitors and became synonymous with database applications of the era.

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


class DBase3Theme(Theme):
    """
    Ashton-Tate dBASE III and dBASE III Plus theme (1984-1985).

    Recreates the iconic cyan menu highlighting on black background that became
    synonymous with database applications in the mid-1980s.

    Visual Identity:
        - Cyan highlighting for menus and interactive elements (dBASE's signature color)
        - Green text for data entry fields (common in custom dBASE applications)
        - White command-line text on black background (the iconic dot prompt)
        - ASCII borders matching dBASE's simple box-drawing style
    """

    # dBASE III color palette
    BLACK = (0, 0, 0)  # #000000
    WHITE = (255, 255, 255)  # #FFFFFF
    CYAN = (0, 255, 255)  # #00FFFF - dBASE's signature menu color
    GREEN = (0, 255, 0)  # #00FF00 - for data entry fields
    RED = (255, 0, 0)  # #FF0000
    YELLOW = (255, 255, 0)  # #FFFF00

    def __init__(self):
        """Initialize the dBASE III theme."""
        super().__init__(
            name="dBASE III",
            description="Ashton-Tate dBASE III theme with cyan menus on black background",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """
        Get background color pair: WHITE on BLACK.

        The classic dBASE dot prompt interface.
        """
        return ColorPair(self.WHITE, self.BLACK)

    def get_button(self) -> ColorPair:
        """
        Get button color pair: CYAN on BLACK.

        dBASE's distinctive menu color that became iconic in the database world.
        """
        return ColorPair(self.CYAN, self.BLACK)

    def get_button_focused(self) -> ColorPair:
        """
        Get focused button color pair: BLACK on CYAN.

        Inverted selection highlighting for menu items and buttons.
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_text_input(self) -> ColorPair:
        """
        Get text input color pair: GREEN on BLACK.

        Distinguishes data entry fields, a common pattern in custom
        dBASE III applications.
        """
        return ColorPair(self.GREEN, self.BLACK)

    def get_border(self) -> ColorPair:
        """Get border color pair: WHITE on BLACK."""
        return ColorPair(self.WHITE, self.BLACK)

    def get_selection(self) -> ColorPair:
        """
        Get selection color pair: BLACK on CYAN.

        Highlighted database records and menu items.
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: BLACK on BLACK.

        Invisible disabled menu items (dBASE convention).
        """
        return ColorPair(self.BLACK, self.BLACK)

    def get_border_chars(self) -> str:
        """
        Get ASCII border characters matching dBASE III's simple box-drawing style.

        Returns:
            String with 8 ASCII characters for box-drawing
        """
        return "+-+||+-+"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the dBASE III theme.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: White on black (dot prompt)
            "background": self.BLACK,
            "foreground": self.WHITE,
            # Primary/Button: Cyan on black (signature dBASE menu color)
            "primary": self.CYAN,
            # Success/TextInput: Green on black (data entry)
            "success": self.GREEN,
            # Error: Red on black
            "error": self.RED,
            # Warning: Yellow on black
            "warning": self.YELLOW,
            # Info: Cyan on black (same as primary)
            "info": self.CYAN,
            # Accent: Cyan (matches primary/buttons)
            "accent": self.CYAN,
        }
