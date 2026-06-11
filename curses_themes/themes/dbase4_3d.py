#!/usr/bin/env python3
"""
Ashton-Tate/Borland dBASE IV 3D windowed interface theme.

Recreates the revolutionary 3D windowed interface of dBASE IV's Control Center
(1988-1993), which introduced drop shadows, raised buttons, and multiple overlapping
windows to DOS-era database applications.

Historical Context:
    dBASE IV (released October 1988) marked a paradigm shift from the command-line
    focus of dBASE III to a fully windowed, mouse-driven interface. The "Control Center"
    introduced a graphical desktop metaphor with pull-down menus, dialog boxes, and
    overlapping windows - revolutionary features for a DOS application.

    The 3D visual effects (drop shadows, raised buttons, sunken input fields) were
    inspired by Borland's Turbo Vision framework and competed directly with early
    Windows applications. Windows had drop shadows that gave depth to the interface,
    making it feel more modern and easier to understand spatial relationships.

    Despite initial bugs that plagued the 1.0 release, dBASE IV eventually stabilized
    and was acquired by Borland in 1991. Its windowed interface influenced database
    tools throughout the 1990s, and the blue-and-white color scheme with 3D effects
    became iconic in the Borland product line.

3D Visual Effects:
    - Drop Shadows: Windows cast 2-pixel horizontal, 1-pixel vertical shadows
    - Raised Buttons: Yellow buttons appear raised above the blue background
    - Sunken Input: Cyan input fields appear recessed into the surface
    - Window Borders: White borders with highlight/lowlight create beveled edges
    - Double Borders: Emphasized dialogs use double-line box characters

    The shadow offset (2h, 1v) matches Borland Turbo Vision's standard shadow
    positioning, creating a consistent look with other Borland tools.

Color Scheme:
    - Background: White on Blue - the Control Center's main interface
    - Button: Yellow on Blue - menu items appear as raised tabs
    - ButtonFocused: Blue on Yellow - inverted selection with 3D highlight
    - TextInput: Cyan on Blue - recessed data entry fields
    - Border: White on Blue - window frames with beveled edges
    - Selection: Blue on White - highlighted records in browse mode
    - Shadow: Black on Black - drop shadow beneath windows
    - Highlight: White on White - bright edges of raised elements
    - Lowlight: Black on Blue - shadow edges of beveled frames

Difference from Flat dBASE IV Theme:
    The standard DBase4Theme recreates the flat, 2D Control Center appearance.
    This 3D variant adds depth through shadows and highlights, matching the
    optional 3D mode available in dBASE IV and the style standardized by
    Borland after their 1991 acquisition.

When to Use:
    - Database management interfaces requiring clear window hierarchy
    - Applications with multiple overlapping windows or dialogs
    - Retro business applications evoking the late-1980s/early-1990s era
    - Tools targeting users familiar with Borland/dBASE products
    - Any interface where spatial depth aids usability

Technical Requirements:
    - EGA or better graphics adapter (VGA recommended for full color palette)
    - 80×25 text mode minimum (80×43/50 for enhanced display)
    - Terminal supporting Unicode box-drawing characters for authentic borders

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

from ..theme import ColorPair
from ..theme3d import Theme3D


class DBase4_3DTheme(Theme3D):
    """
    Ashton-Tate/Borland dBASE IV 3D windowed interface theme (1988-1993).

    Recreates the sophisticated 3D Control Center with drop shadows, raised buttons,
    and beveled window frames that made dBASE IV's interface revolutionary for its era.

    Visual Identity:
        - Blue background matching the Control Center's professional appearance
        - Yellow menu buttons with raised 3D effect
        - White window borders with highlight/lowlight beveling
        - Drop shadows (2 horizontal, 1 vertical) beneath all windows
        - Double-line borders for emphasized dialogs
        - Cyan recessed input fields for data entry

    3D Effects:
        This theme extends the flat dBASE IV appearance with true 3D visual depth,
        matching the optional 3D mode and Borland's post-1991 standardized style.
    """

    # dBASE IV 3D color palette
    BLACK = (0, 0, 0)  # #000000 - shadows and lowlights
    BLUE = (0, 0, 238)  # #0000EE - Control Center blue background
    WHITE = (255, 255, 255)  # #FFFFFF - highlights and borders
    YELLOW = (255, 255, 0)  # #FFFF00 - raised menu buttons
    CYAN = (0, 255, 255)  # #00FFFF - sunken input fields
    RED = (255, 0, 0)  # #FF0000 - error messages
    GREEN = (0, 255, 0)  # #00FF00 - success indicators

    def __init__(self):
        """Initialize the dBASE IV 3D theme."""
        super().__init__(
            name="dBASE IV 3D",
            description="Ashton-Tate/Borland dBASE IV 3D windowed Control Center with drop shadows and beveled frames",
            author="FlossWare",
        )

    def get_background(self) -> ColorPair:
        """
        Get background color pair: WHITE on BLUE.

        The Control Center's signature blue background with white text,
        providing the base surface for 3D elements to rise from or sink into.
        """
        return ColorPair(self.WHITE, self.BLUE)

    def get_button(self) -> ColorPair:
        """
        Get button color pair: YELLOW on BLUE.

        Raised menu buttons and tabs in the iconic dBASE IV yellow.
        The yellow foreground creates the illusion of raised surfaces
        above the blue background.
        """
        return ColorPair(self.YELLOW, self.BLUE)

    def get_button_focused(self) -> ColorPair:
        """
        Get focused button color pair: BLUE on YELLOW.

        Inverted menu selection with enhanced 3D effect. The color inversion
        combined with highlight/lowlight borders creates a visually "pressed"
        button appearance.
        """
        return ColorPair(self.BLUE, self.YELLOW)

    def get_text_input(self) -> ColorPair:
        """
        Get text input color pair: CYAN on BLUE.

        Sunken data entry fields that appear recessed into the interface.
        The cyan color distinguishes input areas from display-only text
        while the visual depth suggests "entering" data into the surface.
        """
        return ColorPair(self.CYAN, self.BLUE)

    def get_border(self) -> ColorPair:
        """
        Get border color pair: WHITE on BLUE.

        Window frames with beveled edges using highlight/lowlight. White borders
        provide the base for 3D beveling, with get_highlight() and get_lowlight()
        adding the raised appearance.
        """
        return ColorPair(self.WHITE, self.BLUE)

    def get_selection(self) -> ColorPair:
        """
        Get selection color pair: BLUE on WHITE.

        Highlighted records in browse mode and selected list items. The inverted
        colors create high contrast while maintaining the blue/white theme consistency.
        """
        return ColorPair(self.BLUE, self.WHITE)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: BLUE on BLUE.

        Dimmed unavailable menu items. The monochromatic appearance creates a
        subtle "grayed out" effect that indicates non-interactive elements without
        completely hiding them.
        """
        return ColorPair(self.BLUE, self.BLUE)

    def get_shadow_color(self) -> ColorPair:
        """
        Get shadow color pair: BLACK on BLACK.

        Drop shadow beneath windows and dialogs. Rendered 2 pixels to the right
        and 1 pixel down from the window edge, matching Borland Turbo Vision's
        standard shadow offset.

        Returns:
            ColorPair for rendering drop shadows
        """
        return ColorPair(self.BLACK, self.BLACK)

    def get_highlight_color(self) -> ColorPair:
        """
        Get highlight color pair: WHITE on WHITE.

        Bright edges of raised elements (top and left borders). Creates the
        illusion of light source from upper-left, making buttons and frames
        appear to rise above the surface.

        Returns:
            ColorPair for rendering bright beveled edges
        """
        return ColorPair(self.WHITE, self.WHITE)

    def get_lowlight_color(self) -> ColorPair:
        """
        Get lowlight color pair: BLACK on BLUE.

        Shadow edges of beveled frames (bottom and right borders). Complements
        highlights to create full 3D beveled effect, suggesting depth and
        dimensionality.

        Returns:
            ColorPair for rendering shadow beveled edges
        """
        return ColorPair(self.BLACK, self.BLUE)

    def get_shadow_offset(self) -> tuple[int, int]:
        """
        Get shadow offset in characters.

        Returns the standard Borland Turbo Vision shadow offset: 2 characters
        horizontal (right), 1 character vertical (down). This creates the
        characteristic drop shadow effect of dBASE IV and other Borland products.

        Returns:
            Tuple of (horizontal_offset, vertical_offset) in character cells
        """
        return (2, 1)

    def get_border_chars(self) -> str:
        """
        Get Unicode single-line border characters.

        Returns the standard Unicode box-drawing characters for single-line borders,
        matching the authentic dBASE IV Control Center window frames.

        Returns:
            String with 8 characters: TL T TR L R BL B BR
            "┌─┐││└─┘" - Unicode single-line box-drawing
        """
        return "┌─┐││└─┘"

    def get_double_border_chars(self) -> str:
        """
        Get Unicode double-line border characters.

        Used for emphasized dialogs, alerts, and primary windows. The double-line
        borders were used in dBASE IV to distinguish important system dialogs from
        regular windows.

        Returns:
            String with 8 characters: TL T TR L R BL B BR
            "╔═╗║║╚═╝" - Unicode double-line box-drawing
        """
        return "╔═╗║║╚═╝"

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for the dBASE IV 3D theme.

        Provides the semantic color mapping required by the Theme base class,
        translating the dBASE IV visual language into standard theme semantics.

        Returns:
            Dictionary mapping semantic color names to RGB tuples
        """
        return {
            # Background: White on blue (Control Center)
            "background": self.BLUE,
            "foreground": self.WHITE,
            # Primary/Button: Yellow on blue (raised menu buttons)
            "primary": self.YELLOW,
            # Success: Green on blue (operation completed successfully)
            "success": self.GREEN,
            # Error: Red on blue (critical errors and warnings)
            "error": self.RED,
            # Warning: Yellow on blue (caution messages, same as primary)
            "warning": self.YELLOW,
            # Info: Cyan on blue (informational messages, matches text input)
            "info": self.CYAN,
            # Accent: Yellow (matches buttons/menus for consistency)
            "accent": self.YELLOW,
        }
