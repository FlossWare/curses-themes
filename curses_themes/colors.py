#!/usr/bin/env python3
"""
Color management and terminal capability detection for curses themes.

This module handles the complexities of terminal color support, including
detection of 8/16/256 color capabilities and RGB-to-palette conversion.

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

import curses
from typing import Optional

from .theme import ComponentColors, SemanticColors


class ColorManager:
    """
    Manages color initialization and terminal capability detection.

    This class handles the complexities of working with different terminal
    color capabilities (8, 16, or 256 colors) and converts RGB values to
    appropriate curses color pairs.

    Example:
        ```python
        def main(stdscr):
            manager = ColorManager(stdscr)
            colors = manager.initialize_theme(my_theme)
            stdscr.addstr(0, 0, "Hello", curses.color_pair(colors.primary))
        ```

    Attributes:
        stdscr: The curses window object
        color_count: Number of colors supported (8, 16, or 256)
    """

    # Standard 8-color palette (ANSI colors)
    BASIC_COLORS = {
        curses.COLOR_BLACK: (0, 0, 0),
        curses.COLOR_RED: (205, 0, 0),
        curses.COLOR_GREEN: (0, 205, 0),
        curses.COLOR_YELLOW: (205, 205, 0),
        curses.COLOR_BLUE: (0, 0, 238),
        curses.COLOR_MAGENTA: (205, 0, 205),
        curses.COLOR_CYAN: (0, 205, 205),
        curses.COLOR_WHITE: (229, 229, 229),
    }

    # Next color pair number to allocate
    _next_pair = 1

    # Cache of (fg_color, bg_color) -> pair_num to reuse existing pairs
    _pair_cache: dict[tuple[int, int], int] = {}

    def __init__(self, stdscr):
        """
        Initialize color manager for a curses screen.

        Args:
            stdscr: Curses window object (typically from curses.wrapper)

        Raises:
            RuntimeError: If the terminal doesn't support colors
        """
        self.stdscr = stdscr

        if not curses.has_colors():
            raise RuntimeError(
                "Terminal does not support colors. "
                "Please use a color-capable terminal emulator."
            )

        curses.start_color()
        curses.use_default_colors()

        self.color_count = self._detect_color_capability()

    def _detect_color_capability(self) -> int:
        """
        Detect terminal color support level.

        Returns:
            Number of colors supported: 8, 16, or 256

        Note:
            Some terminals report more colors than they actually support well.
            This method provides conservative detection.
        """
        max_colors = curses.COLORS

        if max_colors >= 256:
            return 256
        elif max_colors >= 16:
            return 16
        else:
            return 8

    def _rgb_to_curses_color(self, r: int, g: int, b: int) -> int:
        """
        Convert RGB values to a curses color number.

        Adapts to terminal capabilities by mapping to 256-color palette,
        16-color palette, or 8-color palette as appropriate.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Curses color number appropriate for terminal capability
        """
        if self.color_count >= 256:
            return self._rgb_to_256(r, g, b)
        else:
            return self._rgb_to_basic(r, g, b)

    def _rgb_to_256(self, r: int, g: int, b: int) -> int:
        """
        Map RGB to 256-color palette.

        Uses the standard xterm 256-color palette:
        - Colors 0-15: System colors
        - Colors 16-231: 6x6x6 RGB cube
        - Colors 232-255: Grayscale ramp

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Color number in range 0-255
        """
        # Check if it's a grayscale color
        if r == g == b:
            # Use grayscale ramp (232-255)
            if r < 8:
                return 16  # Black
            if r > 247:
                return 231  # White
            return 232 + (r - 8) // 10

        # Map to 6x6x6 RGB cube (16-231)
        # Each component mapped to 0-5
        r_index = (r * 6) // 256
        g_index = (g * 6) // 256
        b_index = (b * 6) // 256

        return 16 + (36 * r_index) + (6 * g_index) + b_index

    def _rgb_to_basic(self, r: int, g: int, b: int) -> int:
        """
        Map RGB to 8 or 16 basic ANSI colors.

        Finds the closest match in the basic color palette using
        simple Euclidean distance in RGB space.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Basic curses color constant (COLOR_BLACK, COLOR_RED, etc.)
        """
        min_distance = float("inf")
        closest_color = curses.COLOR_WHITE

        for color, (cr, cg, cb) in self.BASIC_COLORS.items():
            # Euclidean distance in RGB space
            distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_color = color

        return closest_color

    def _init_color_pair(
        self,
        fg_rgb: tuple[int, int, int],
        bg_rgb: Optional[tuple[int, int, int]] = None,
    ) -> int:
        """
        Initialize a curses color pair from RGB values.

        Args:
            fg_rgb: Foreground RGB tuple (R, G, B)
            bg_rgb: Background RGB tuple, or None for default background

        Returns:
            Color pair number that can be used with curses.color_pair()
        """
        fg_color = self._rgb_to_curses_color(*fg_rgb)

        if bg_rgb is None:
            bg_color = -1  # Use default background
        else:
            bg_color = self._rgb_to_curses_color(*bg_rgb)

        # Check cache first to reuse existing pair for same color combination
        cache_key = (fg_color, bg_color)
        if cache_key in ColorManager._pair_cache:
            return ColorManager._pair_cache[cache_key]

        pair_num = ColorManager._next_pair
        ColorManager._next_pair += 1

        # Ensure we don't exceed curses color pair limit
        if pair_num >= curses.COLOR_PAIRS:
            raise RuntimeError(
                f"Exceeded maximum color pairs ({curses.COLOR_PAIRS}). "
                "Too many themes or colors in use."
            )

        try:
            curses.init_pair(pair_num, fg_color, bg_color)
        except curses.error as e:
            raise RuntimeError(
                f"Failed to initialize color pair {pair_num} "
                f"(fg={fg_color}, bg={bg_color}): {e}"
            )

        # Cache the pair for future reuse
        ColorManager._pair_cache[cache_key] = pair_num

        return pair_num

    def initialize_theme(self, theme) -> tuple[SemanticColors, ComponentColors]:
        """
        Initialize all color pairs for a theme.

        Converts the theme's RGB color map and component colors to curses
        color pairs appropriate for the terminal's capabilities.

        Args:
            theme: Theme instance with get_color_map() and component methods

        Returns:
            Tuple of (SemanticColors, ComponentColors) with initialized color pair numbers

        Raises:
            ValueError: If color map is missing required keys
            RuntimeError: If color initialization fails
        """
        color_map = theme.get_color_map()

        # Validate required colors
        required_colors = {
            "background",
            "foreground",
            "primary",
            "success",
            "error",
            "warning",
            "info",
            "accent",
        }
        missing = required_colors - set(color_map.keys())
        if missing:
            raise ValueError(f"Theme '{theme.name}' missing required colors: {missing}")

        # Get background RGB for all pairs
        bg_rgb = color_map["background"]

        # Initialize color pairs for each semantic color
        # Background pair uses default background for transparency
        background_pair = self._init_color_pair(color_map["foreground"], bg_rgb)

        # All other colors use the theme's background
        semantic_colors = SemanticColors(
            primary=self._init_color_pair(color_map["primary"], bg_rgb),
            success=self._init_color_pair(color_map["success"], bg_rgb),
            error=self._init_color_pair(color_map["error"], bg_rgb),
            warning=self._init_color_pair(color_map["warning"], bg_rgb),
            info=self._init_color_pair(color_map["info"], bg_rgb),
            background=background_pair,
            foreground=self._init_color_pair(color_map["foreground"], bg_rgb),
            accent=self._init_color_pair(color_map["accent"], bg_rgb),
        )

        # Initialize component-based color pairs from theme methods
        component_colors = ComponentColors(
            background=self._init_color_pair_from_colorpair(theme.get_background()),
            button=self._init_color_pair_from_colorpair(theme.get_button()),
            button_focused=self._init_color_pair_from_colorpair(
                theme.get_button_focused()
            ),
            text_input=self._init_color_pair_from_colorpair(theme.get_text_input()),
            border=self._init_color_pair_from_colorpair(theme.get_border()),
            selection=self._init_color_pair_from_colorpair(theme.get_selection()),
            disabled=self._init_color_pair_from_colorpair(theme.get_disabled()),
        )

        return semantic_colors, component_colors

    def _init_color_pair_from_colorpair(self, color_pair) -> int:
        """
        Initialize a curses color pair from a ColorPair object.

        Args:
            color_pair: ColorPair with foreground and background RGB tuples

        Returns:
            Color pair number that can be used with curses.color_pair()
        """
        return self._init_color_pair(color_pair.foreground, color_pair.background)

    def reset(self) -> None:
        """
        Reset color pair counter.

        This is primarily for testing. In normal use, color pairs persist
        for the lifetime of the curses session.
        """
        ColorManager._next_pair = 1
        ColorManager._pair_cache.clear()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ColorManager(colors={self.color_count})"
