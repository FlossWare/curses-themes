#!/usr/bin/env python3
"""
3D theming support for curses applications.

This module extends the base Theme class with 3D rendering capabilities,
including shadow effects, highlight/lowlight edges, and raised/sunken borders.
The 3D effect creates a visual illusion of depth through careful use of
highlight and shadow colors, mimicking the beveled interfaces popularized
by GUI frameworks in the late 1980s and early 1990s.

Rendering Technique:
    3D effects are achieved through three key color components:
    - Highlight: Bright edge color for the top and left edges of raised elements
    - Lowlight: Medium edge color for the bottom and right edges of raised elements
    - Shadow: Dark color cast behind elements to create depth illusion

    For raised elements (buttons, panels), the highlight appears on top/left
    while lowlight appears on bottom/right. For sunken elements (text inputs),
    these colors are reversed to create an inset appearance.

Historical Context:
    The 3D beveled interface style originated with Apple's Macintosh (1984)
    and became ubiquitous through frameworks like Microsoft Windows 3.x (1990),
    Borland's Turbo Vision (1990), and Motif. This visual language dominated
    GUI design throughout the 1990s before being largely displaced by flat
    design in the 2010s.

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

import contextlib
import curses
from typing import Optional

from .theme import ColorPair, Theme


class Theme3D(Theme):
    """
    Abstract base class for themes with 3D rendering capabilities.

    Extends the base Theme class with methods for creating 3D visual effects
    through highlights, lowlights, and drop shadows. Provides draw_box_3d()
    for rendering beveled borders with depth.

    Subclasses must implement:
        - get_color_map(): Define base color palette (from Theme)
        - get_shadow_color(): Define shadow color for drop shadows
        - get_highlight_color(): Define bright edge color for raised surfaces
        - get_lowlight_color(): Define dark edge color for raised surfaces

    Optional customization:
        - shadow_offset_x: Horizontal shadow offset (default: 2)
        - shadow_offset_y: Vertical shadow offset (default: 1)
        - get_double_border_chars(): Double-line border style (default: "╔═╗║║╚═╝")

    Example:
        ```python
        class My3DTheme(Theme3D):
            def __init__(self):
                super().__init__(
                    name="My 3D Theme",
                    description="A custom 3D theme",
                    author="Your Name"
                )

            def get_shadow_color(self):
                return ColorPair((0, 0, 0), (0, 0, 0))  # Black shadow

            def get_highlight_color(self):
                return ColorPair((255, 255, 255), (200, 200, 200))  # White highlight

            def get_lowlight_color(self):
                return ColorPair((64, 64, 64), (200, 200, 200))  # Dark gray lowlight

            def get_color_map(self):
                return {
                    'background': (200, 200, 200),
                    'foreground': (0, 0, 0),
                    # ... rest of color map
                }
        ```

    Attributes:
        shadow_offset_x: Horizontal offset for drop shadows (default: 2)
        shadow_offset_y: Vertical offset for drop shadows (default: 1)
    """

    def __init__(self, name: str, description: str = "", author: str = ""):
        """
        Initialize 3D theme metadata.

        Args:
            name: Human-readable theme name
            description: Brief description of the theme's appearance or purpose
            author: Name of the theme creator
        """
        super().__init__(name, description, author)
        self._shadow_offset_x = 2
        self._shadow_offset_y = 1
        self._shadow_color_pair: Optional[int] = None
        self._highlight_color_pair: Optional[int] = None
        self._lowlight_color_pair: Optional[int] = None

    @property
    def shadow_offset_x(self) -> int:
        """
        Get horizontal shadow offset.

        Returns:
            Number of characters to offset shadow horizontally (default: 2)
        """
        return self._shadow_offset_x

    @shadow_offset_x.setter
    def shadow_offset_x(self, value: int) -> None:
        """
        Set horizontal shadow offset.

        Args:
            value: Number of characters to offset shadow horizontally
        """
        if value < 0:
            raise ValueError("Shadow offset must be non-negative")
        self._shadow_offset_x = value

    @property
    def shadow_offset_y(self) -> int:
        """
        Get vertical shadow offset.

        Returns:
            Number of lines to offset shadow vertically (default: 1)
        """
        return self._shadow_offset_y

    @shadow_offset_y.setter
    def shadow_offset_y(self, value: int) -> None:
        """
        Set vertical shadow offset.

        Args:
            value: Number of lines to offset shadow vertically
        """
        if value < 0:
            raise ValueError("Shadow offset must be non-negative")
        self._shadow_offset_y = value

    def get_shadow_color(self) -> ColorPair:
        """
        Get the shadow color for drop shadows.

        This color is used to render the shadow cast behind 3D elements,
        creating the illusion of depth. Typically a dark or black color.

        Returns:
            ColorPair for shadow rendering

        Note:
            Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement get_shadow_color()")

    def get_highlight_color(self) -> ColorPair:
        """
        Get the highlight color for raised edges.

        This color is used on the top and left edges of raised elements
        (buttons, panels) to simulate light reflection. Typically a bright
        color, often white or a lighter shade of the base color.

        Returns:
            ColorPair for highlight edge rendering

        Note:
            Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement get_highlight_color()")

    def get_lowlight_color(self) -> ColorPair:
        """
        Get the lowlight color for shaded edges.

        This color is used on the bottom and right edges of raised elements
        to simulate shadow on the surface itself. Typically a darker shade
        of the base color, distinct from the drop shadow.

        Returns:
            ColorPair for lowlight edge rendering

        Note:
            Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement get_lowlight_color()")

    def get_double_border_chars(self) -> str:
        """
        Get double-line border characters for 3D boxes.

        Returns Unicode double-line box-drawing characters that create
        a heavier, more pronounced border suitable for 3D effects.

        Returns:
            String with 8 characters in order:
            top-left, top, top-right, left, right, bottom-left, bottom, bottom-right
            Default: "╔═╗║║╚═╝" (Unicode double-line box)

        Note:
            Override this method to provide custom double-border styles.
        """
        return "╔═╗║║╚═╝"

    def supports_3d(self) -> bool:
        """
        Check if this theme supports 3D rendering.

        Returns:
            True (Theme3D always supports 3D rendering)
        """
        return True

    def apply(self, stdscr) -> None:
        """
        Apply this theme to a curses screen, including 3D color pairs.

        Initializes standard theme colors plus shadow, highlight, and lowlight
        color pairs for 3D rendering.

        Args:
            stdscr: Curses window object (typically from curses.wrapper)

        Raises:
            RuntimeError: If color initialization fails
        """
        # Initialize base theme colors
        super().apply(stdscr)

        # Initialize 3D-specific color pairs
        from .colors import ColorManager

        color_manager = ColorManager(stdscr)

        shadow = self.get_shadow_color()
        highlight = self.get_highlight_color()
        lowlight = self.get_lowlight_color()

        self._shadow_color_pair = color_manager._init_color_pair(
            shadow.foreground, shadow.background
        )
        self._highlight_color_pair = color_manager._init_color_pair(
            highlight.foreground, highlight.background
        )
        self._lowlight_color_pair = color_manager._init_color_pair(
            lowlight.foreground, lowlight.background
        )

    @property
    def shadow_color_pair(self) -> int:
        """
        Get shadow color pair number.

        Returns:
            Curses color pair number for shadow rendering

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._shadow_color_pair is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._shadow_color_pair

    @property
    def highlight_color_pair(self) -> int:
        """
        Get highlight color pair number.

        Returns:
            Curses color pair number for highlight edge rendering

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._highlight_color_pair is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._highlight_color_pair

    @property
    def lowlight_color_pair(self) -> int:
        """
        Get lowlight color pair number.

        Returns:
            Curses color pair number for lowlight edge rendering

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._lowlight_color_pair is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._lowlight_color_pair

    def draw_box_3d(
        self,
        window,
        y: int,
        x: int,
        height: int,
        width: int,
        raised: bool = True,
        title: str = "",
    ) -> None:
        """
        Draw a 3D bordered box with beveled edges and drop shadow.

        Creates a box with highlight/lowlight edges to simulate depth.
        Raised boxes appear to protrude from the screen (for buttons, panels),
        while sunken boxes appear recessed (for text inputs).

        The box is rendered in multiple layers:
        1. Drop shadow (behind the box, offset by shadow_offset_x/y)
        2. Main border (using theme border color)
        3. Highlight edge (top and left for raised, bottom and right for sunken)
        4. Lowlight edge (bottom and right for raised, top and left for sunken)

        Args:
            window: Curses window to draw on
            y: Top-left Y coordinate of the box (not including shadow)
            x: Top-left X coordinate of the box (not including shadow)
            height: Box height in characters
            width: Box width in characters
            raised: If True, draw raised (button style); if False, draw sunken (input style)
            title: Optional title to display centered in top border

        Raises:
            ValueError: If box dimensions are too small
            RuntimeError: If theme has not been applied

        Example:
            ```python
            # Draw a raised button
            theme.draw_box_3d(window, 5, 10, 3, 20, raised=True, title="OK")

            # Draw a sunken text input
            theme.draw_box_3d(window, 10, 10, 3, 30, raised=False)
            ```

        Note:
            Ensure sufficient space for the shadow by leaving shadow_offset_x
            columns on the right and shadow_offset_y rows on the bottom.
        """
        if height < 2 or width < 2:
            raise ValueError(
                f"Box dimensions too small: {height}x{width}. Minimum is 2x2."
            )

        border_chars = self.get_border_chars()
        if len(border_chars) != 8:
            raise ValueError(
                f"get_border_chars() must return 8 characters, got {len(border_chars)}"
            )

        # Parse border characters: TL T TR L R BL B BR
        top_left, top, top_right, left, right, bottom_left, bottom, bottom_right = (
            tuple(border_chars)
        )

        # Draw drop shadow first (behind the box)
        if self.shadow_offset_x > 0 or self.shadow_offset_y > 0:
            shadow_attr = curses.color_pair(self.shadow_color_pair)
            shadow_y = y + self.shadow_offset_y
            shadow_x = x + self.shadow_offset_x

            # Draw shadow on right edge
            if self.shadow_offset_x > 0:
                for i in range(height):
                    for j in range(self.shadow_offset_x):
                        with contextlib.suppress(curses.error):
                            window.addch(
                                shadow_y + i, shadow_x + width + j, " ", shadow_attr
                            )

            # Draw shadow on bottom edge
            if self.shadow_offset_y > 0:
                for i in range(self.shadow_offset_y):
                    for j in range(width + self.shadow_offset_x):
                        with contextlib.suppress(curses.error):
                            window.addch(
                                shadow_y + height + i, shadow_x + j, " ", shadow_attr
                            )

        # Draw main border
        border_attr = curses.color_pair(self.components.border)

        # Draw corners
        try:
            window.addstr(y, x, top_left, border_attr)
            window.addstr(y, x + width - 1, top_right, border_attr)
            window.addstr(y + height - 1, x, bottom_left, border_attr)
            window.addstr(y + height - 1, x + width - 1, bottom_right, border_attr)
        except curses.error:
            pass

        # Draw horizontal borders
        for i in range(1, width - 1):
            try:
                window.addstr(y, x + i, top, border_attr)
                window.addstr(y + height - 1, x + i, bottom, border_attr)
            except curses.error:
                pass

        # Draw vertical borders
        for i in range(1, height - 1):
            try:
                window.addstr(y + i, x, left, border_attr)
                window.addstr(y + i, x + width - 1, right, border_attr)
            except curses.error:
                pass

        # Draw 3D beveled edges
        if raised:
            # Raised: highlight on top/left, lowlight on bottom/right
            highlight_attr = curses.color_pair(self.highlight_color_pair)
            lowlight_attr = curses.color_pair(self.lowlight_color_pair)

            # Highlight top edge (just inside the border)
            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + 1, x + i, " ", highlight_attr)

            # Highlight left edge (just inside the border)
            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + 1, " ", highlight_attr)

            # Lowlight bottom edge (just inside the border)
            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + height - 2, x + i, " ", lowlight_attr)

            # Lowlight right edge (just inside the border)
            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + width - 2, " ", lowlight_attr)
        else:
            # Sunken: lowlight on top/left, highlight on bottom/right (reversed)
            highlight_attr = curses.color_pair(self.highlight_color_pair)
            lowlight_attr = curses.color_pair(self.lowlight_color_pair)

            # Lowlight top edge
            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + 1, x + i, " ", lowlight_attr)

            # Lowlight left edge
            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + 1, " ", lowlight_attr)

            # Highlight bottom edge
            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + height - 2, x + i, " ", highlight_attr)

            # Highlight right edge
            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + width - 2, " ", highlight_attr)

        # Draw title if provided
        if title and width > len(title) + 4:
            title_x = x + (width - len(title) - 2) // 2
            with contextlib.suppress(curses.error):
                window.addstr(y, title_x, f" {title} ", border_attr)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Theme3D(name='{self.name}', author='{self.author}')"
