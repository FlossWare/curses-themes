#!/usr/bin/env python3
"""
Borland Turbo Vision 3D theme.

Recreates the iconic blue-and-cyan 3D interface of Borland Turbo Vision (1990),
one of the most influential text-mode UI frameworks of the early 1990s. This
theme captures the distinctive raised-button aesthetic that made Turbo Pascal,
Turbo C++, and other Borland tools instantly recognizable.

Historical Context:
    Borland Turbo Vision, released in 1990 for MS-DOS, revolutionized text-mode
    user interfaces by bringing GUI-like elements to character-based terminals.
    Its distinctive blue background with cyan highlights, 3D beveled buttons,
    and shadow effects became the visual identity of professional development
    tools throughout the early 1990s.

    Key Borland products using this interface:
    - Turbo Pascal 6.0+ (1990-1992)
    - Turbo C++ 1.0+ (1990-1992)
    - Borland C++ 2.0+ (1991-1997)
    - Borland Pascal 7.0 (1992)
    - Turbo Assembler IDE (1989-1993)

    The framework was so influential that it was open-sourced in 2000 and
    continues to inspire retro computing enthusiasts today. Many developers
    who learned programming in the 1990s remember the Turbo Vision interface
    with deep nostalgia.

Visual Design Philosophy:
    Turbo Vision's 3D effect was achieved through careful color selection:
    - Blue background (#0000AA) provided a professional, calming base
    - Cyan (#00AAAA) was used for raised surfaces and focus indication
    - White highlights on cyan created the illusion of light reflection
    - Black lowlights on cyan simulated shadow on the beveled edge
    - Drop shadows (black on blue) added depth to floating windows

    This color scheme was optimized for CGA/EGA/VGA displays and looked
    equally good on both color and monochrome monitors (where it appeared
    as varying shades of gray).

Technical Authenticity:
    This implementation uses the authentic Turbo Vision color palette:
    - Background: Yellow text on Blue (#0000AA)
    - Buttons: Cyan text on Blue
    - Focused Buttons: Black text on Cyan (#00AAAA) with white/black bevels
    - Highlight edges: White on Cyan (simulating light reflection)
    - Lowlight edges: Black on Cyan (simulating shadow)
    - Drop shadow: Black on Black (offset 2 horizontal, 1 vertical)

    Border characters use rounded corners (╭─╮) matching Turbo Vision's
    friendly aesthetic, while double borders (╔═╗) are available for
    dialog boxes and emphasized panels.

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

from typing import Dict, Tuple
from ..theme3d import Theme3D
from ..theme import ColorPair


class Borland3DTheme(Theme3D):
    """
    Borland Turbo Vision 3D theme (1990-1997).

    Recreates the distinctive blue-and-cyan interface with 3D beveled buttons
    and drop shadows that defined Borland's professional development tools.

    Visual Identity:
        - Deep blue background (#0000AA) - the signature Turbo Vision color
        - Cyan raised surfaces (#00AAAA) - for buttons and focused elements
        - White highlights and black lowlights - creating the 3D bevel effect
        - Rounded borders with Unicode box-drawing characters
        - Drop shadows for depth (2 characters horizontal, 1 vertical)

    Color Palette (Authentic Borland):
        - BLUE: RGB(0, 0, 170) - #0000AA - Background color
        - CYAN: RGB(0, 170, 170) - #00AAAA - Button and focus color
        - YELLOW: RGB(255, 255, 85) - #FFFF55 - Text on blue background
        - WHITE: RGB(255, 255, 255) - #FFFFFF - Highlights
        - BLACK: RGB(0, 0, 0) - #000000 - Lowlights and shadows
        - LIGHT_GRAY: RGB(170, 170, 170) - #AAAAAA - Disabled text
        - RED: RGB(255, 85, 85) - #FF5555 - Error messages
        - GREEN: RGB(85, 255, 85) - #55FF55 - Success messages

    Usage Example:
        ```python
        import curses
        from curses_themes.themes.borland3d import Borland3DTheme

        def main(stdscr):
            theme = Borland3DTheme()
            theme.apply(stdscr)

            # Draw a classic Borland-style button
            theme.draw_box_3d(stdscr, 5, 10, 3, 15, raised=True, title="OK")

            # Draw a sunken text input
            theme.draw_box_3d(stdscr, 10, 10, 3, 30, raised=False)

            stdscr.getch()

        curses.wrapper(main)
        ```

    Historical Note:
        The Turbo Vision framework was revolutionary because it provided
        object-oriented UI components in an era when most DOS applications
        were still using procedural code. It demonstrated that professional,
        visually appealing interfaces were possible even in text mode,
        influencing a generation of developers and setting the standard
        for TUI (Text User Interface) design.
    """

    # Authentic Borland Turbo Vision color palette
    # These values match the original CGA/EGA/VGA colors used in Turbo Pascal 6.0+
    BLUE = (0, 0, 170)          # #0000AA - The iconic Borland blue background
    CYAN = (0, 170, 170)        # #00AAAA - Raised buttons and focus color
    YELLOW = (255, 255, 85)     # #FFFF55 - Text on blue (slightly muted for CRT authenticity)
    WHITE = (255, 255, 255)     # #FFFFFF - Bright highlights on bevels
    BLACK = (0, 0, 0)           # #000000 - Shadows and lowlights
    LIGHT_GRAY = (170, 170, 170)  # #AAAAAA - Disabled elements
    RED = (255, 85, 85)         # #FF5555 - Error messages
    GREEN = (85, 255, 85)       # #55FF55 - Success feedback
    MAGENTA = (170, 0, 170)     # #AA00AA - Accent color

    def __init__(self):
        """
        Initialize the Borland Turbo Vision 3D theme.

        Sets up the classic blue-and-cyan color scheme with 3D rendering
        enabled. Shadow offset is configured to match the original Turbo
        Vision appearance (2 horizontal, 1 vertical).
        """
        super().__init__(
            name="Borland 3D",
            description="Borland Turbo Vision 3D theme with beveled buttons and drop shadows (1990-1997)",
            author="FlossWare"
        )
        # Set shadow offsets to match original Turbo Vision
        self.shadow_offset_x = 2
        self.shadow_offset_y = 1

    def get_background(self) -> ColorPair:
        """
        Get background color pair: YELLOW text on BLUE.

        The iconic Borland color scheme - yellow text on deep blue background.
        This combination was chosen for excellent readability on CGA/EGA/VGA
        displays and became synonymous with professional development tools.

        Returns:
            ColorPair with yellow foreground on blue background
        """
        return ColorPair(self.YELLOW, self.BLUE)

    def get_button(self) -> ColorPair:
        """
        Get button color pair: CYAN text on BLUE.

        Buttons in normal (unfocused) state use cyan text to distinguish them
        from regular text while maintaining the blue background theme.

        Returns:
            ColorPair with cyan foreground on blue background
        """
        return ColorPair(self.CYAN, self.BLUE)

    def get_button_focused(self) -> ColorPair:
        """
        Get focused button color pair: BLACK text on CYAN.

        Focused buttons reverse to black-on-cyan, creating the distinctive
        Turbo Vision "raised button" appearance. This is the most iconic
        element of the Borland interface aesthetic.

        Returns:
            ColorPair with black foreground on cyan background
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_text_input(self) -> ColorPair:
        """
        Get text input color pair: BLACK text on CYAN.

        Text input fields use the same colors as focused buttons but are
        rendered with sunken borders (raised=False) to indicate they are
        editable areas.

        Returns:
            ColorPair with black foreground on cyan background
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_border(self) -> ColorPair:
        """
        Get border color pair: CYAN text on BLUE.

        Window borders and frames use cyan to create clear visual separation
        while maintaining harmony with the overall color scheme.

        Returns:
            ColorPair with cyan foreground on blue background
        """
        return ColorPair(self.CYAN, self.BLUE)

    def get_selection(self) -> ColorPair:
        """
        Get selection color pair: BLACK text on CYAN.

        Selected items use inverted colors (black on cyan) to clearly indicate
        the current selection, matching the focused button style.

        Returns:
            ColorPair with black foreground on cyan background
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_disabled(self) -> ColorPair:
        """
        Get disabled color pair: LIGHT_GRAY text on BLUE.

        Disabled elements use light gray text on blue, making them visibly
        distinct from active elements while remaining readable.

        Returns:
            ColorPair with light gray foreground on blue background
        """
        return ColorPair(self.LIGHT_GRAY, self.BLUE)

    def get_shadow_color(self) -> ColorPair:
        """
        Get shadow color pair: BLACK on BLACK.

        Drop shadows use pure black to create the depth illusion. In the
        original Turbo Vision, shadows appeared as dark areas behind windows
        and dialogs.

        Returns:
            ColorPair with black foreground and background
        """
        return ColorPair(self.BLACK, self.BLACK)

    def get_highlight_color(self) -> ColorPair:
        """
        Get highlight color pair: WHITE on CYAN.

        The bright edge of 3D elements uses white on cyan, simulating light
        reflection on the top and left edges of raised buttons. This is the
        key element that creates the 3D beveled appearance.

        Returns:
            ColorPair with white foreground on cyan background
        """
        return ColorPair(self.WHITE, self.CYAN)

    def get_lowlight_color(self) -> ColorPair:
        """
        Get lowlight color pair: BLACK on CYAN.

        The dark edge of 3D elements uses black on cyan, simulating shadow
        on the bottom and right edges of raised buttons. Combined with the
        white highlight, this creates the beveled 3D effect.

        Returns:
            ColorPair with black foreground on cyan background
        """
        return ColorPair(self.BLACK, self.CYAN)

    def get_border_chars(self) -> str:
        """
        Get rounded border characters for the Borland aesthetic.

        Turbo Vision used rounded corners to create a friendly, approachable
        appearance. This matches the original framework's design philosophy
        of making professional tools feel less intimidating.

        Returns:
            String with 8 Unicode characters for rounded box-drawing:
            "╭─╮│╰─╯│" (rounded corners with straight edges)

        Note:
            For dialogs and emphasized panels, use get_double_border_chars()
            which returns double-line borders (╔═╗) for a heavier appearance.
        """
        return "╭─╮│╰─╯│"

    def get_double_border_chars(self) -> str:
        """
        Get double-line border characters for emphasized panels.

        Double borders were used in Turbo Vision for dialog boxes and
        important panels to create visual hierarchy and draw attention.

        Returns:
            String with 8 Unicode characters for double-line box-drawing:
            "╔═╗║║╚═╝" (double-line borders)
        """
        return "╔═╗║║╚═╝"

    def get_color_map(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Get RGB color definitions for the Borland Turbo Vision theme.

        Provides the complete color palette using authentic Borland colors
        from the CGA/EGA/VGA era. These colors were carefully chosen for
        readability, professional appearance, and compatibility with both
        color and monochrome displays.

        Returns:
            Dictionary mapping semantic color names to RGB tuples

        Color Mapping:
            - background: BLUE (#0000AA) - The signature Borland blue
            - foreground: YELLOW (#FFFF55) - Text on blue background
            - primary: CYAN (#00AAAA) - Buttons and interactive elements
            - success: GREEN (#55FF55) - Positive feedback
            - error: RED (#FF5555) - Error messages
            - warning: YELLOW (#FFFF55) - Warnings (same as foreground)
            - info: CYAN (#00AAAA) - Information (same as primary)
            - accent: MAGENTA (#AA00AA) - Special highlights
        """
        return {
            # Background: Yellow text on iconic Borland blue
            'background': self.BLUE,
            'foreground': self.YELLOW,

            # Primary: Cyan for buttons and interactive elements
            'primary': self.CYAN,

            # Success: Green for positive feedback
            'success': self.GREEN,

            # Error: Red for error messages
            'error': self.RED,

            # Warning: Yellow for warnings (matches foreground)
            'warning': self.YELLOW,

            # Info: Cyan for informational messages (matches primary)
            'info': self.CYAN,

            # Accent: Magenta for special highlights
            'accent': self.MAGENTA,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"Borland3DTheme(name='{self.name}', "
            f"shadow_offset=({self.shadow_offset_x}, {self.shadow_offset_y}))"
        )
