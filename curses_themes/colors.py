#!/usr/bin/env python3
"""
Color management and terminal capability detection for curses themes.

This module handles the complexities of terminal color support, including
detection of 8/16/256 color capabilities and RGB-to-palette conversion.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
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

    State Persistence:
        ColorManager uses class-level state (_next_pair and _pair_cache) that
        persists across all instances within a single Python process. This design
        ensures color pairs are never duplicated, even when creating multiple
        ColorManager instances:

        - _next_pair: Class variable tracking the next available color pair number
        - _pair_cache: Class-level dict caching (fg, bg) -> pair_num mappings

        This means:
        1. Creating a new ColorManager(stdscr) does NOT reset color pairs
        2. All ColorManager instances share the same pair allocation pool
        3. Color pairs persist until Python process exits or reset() is called
        4. The reset() method is primarily for testing and should rarely be used

        Example showing persistence:
        ```python
        def part1(stdscr):
            mgr1 = ColorManager(stdscr)
            pair1 = mgr1.init_color_pair((255, 0, 0), (0, 0, 0))  # Returns 1

        def part2(stdscr):
            mgr2 = ColorManager(stdscr)  # New instance
            pair2 = mgr2.init_color_pair((255, 0, 0), (0, 0, 0))  # Returns 1 (cached)
            pair3 = mgr2.init_color_pair((0, 255, 0), (0, 0, 0))  # Returns 2
        ```
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

    # Class-level state persists across all ColorManager instances
    # This ensures color pairs are never duplicated in a single process

    # Next color pair number to allocate (shared across all instances)
    # Starts at 1 since 0 is reserved by curses for default colors
    _next_pair = 1

    # Cache of (fg_color, bg_color) -> pair_num to reuse existing pairs
    # Shared across all instances to prevent duplicate pair allocation
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
            # Use grayscale ramp (232-255), palette values: 8, 18, 28, ..., 238
            if r < 4:
                return 16  # Black
            if r > 246:
                return 231  # White
            return min(232 + (r - 3) // 10, 255)

        # Map to 6x6x6 RGB cube (16-231)
        # Xterm palette values: 0, 95, 135, 175, 215, 255
        # Thresholds are midpoints between adjacent values
        r_index = self._component_to_cube_index(r)
        g_index = self._component_to_cube_index(g)
        b_index = self._component_to_cube_index(b)

        return 16 + (36 * r_index) + (6 * g_index) + b_index

    @staticmethod
    def _component_to_cube_index(v: int) -> int:
        """Map a single RGB component (0-255) to the xterm 6x6x6 cube index (0-5)."""
        if v < 48:
            return 0
        if v < 115:
            return 1
        return (v - 35) // 40

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

    def init_color_pair(
        self,
        fg_rgb: tuple[int, int, int],
        bg_rgb: Optional[tuple[int, int, int]] = None,
    ) -> int:
        """
        Initialize a curses color pair from RGB values.

        Uses class-level cache to reuse existing pairs for identical color
        combinations across all ColorManager instances. This prevents exceeding
        the terminal's COLOR_PAIRS limit.

        Args:
            fg_rgb: Foreground RGB tuple (R, G, B)
            bg_rgb: Background RGB tuple, or None for default background

        Returns:
            Integer color pair number. When using with curses display functions,
            wrap this with curses.color_pair():

            >>> pair_num = manager.init_color_pair((255, 255, 255), (0, 0, 0))
            >>> stdscr.addstr(0, 0, "Text", curses.color_pair(pair_num))

        Note:
            The same color combination always returns the same pair number,
            even across different ColorManager instances, due to class-level
            caching.
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

        # Only consume the slot after successful init
        ColorManager._next_pair += 1

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
            missing_list = ", ".join(sorted(missing))
            raise ValueError(
                f"Theme '{theme.name}' is incomplete - missing required colors: {missing_list}\n"
                f"get_color_map() must return all 8 required colors:\n"
                f"  {', '.join(sorted(required_colors))}\n"
                f"Example:\n"
                f"  def get_color_map(self):\n"
                f"      return {{\n"
                f"          'background': (0, 0, 0),\n"
                f"          'foreground': (255, 255, 255),\n"
                f"          'primary': (0, 120, 215),\n"
                f"          'success': (16, 124, 16),\n"
                f"          'error': (232, 17, 35),\n"
                f"          'warning': (193, 156, 0),\n"
                f"          'info': (0, 120, 212),\n"
                f"          'accent': (142, 68, 173),\n"
                f"      }}"
            )

        # Get background RGB for all pairs
        bg_rgb = color_map["background"]

        # Initialize color pairs for each semantic color
        # Background pair: foreground text on theme background (same as foreground pair)
        background_pair = self.init_color_pair(color_map["foreground"], bg_rgb)

        # All other colors use the theme's background
        semantic_colors = SemanticColors(
            primary=self.init_color_pair(color_map["primary"], bg_rgb),
            success=self.init_color_pair(color_map["success"], bg_rgb),
            error=self.init_color_pair(color_map["error"], bg_rgb),
            warning=self.init_color_pair(color_map["warning"], bg_rgb),
            info=self.init_color_pair(color_map["info"], bg_rgb),
            background=background_pair,
            foreground=self.init_color_pair(color_map["foreground"], bg_rgb),
            accent=self.init_color_pair(color_map["accent"], bg_rgb),
        )

        # Initialize component-based color pairs from theme
        comp_dict = theme.get_components()

        component_colors = ComponentColors(
            background=self._init_color_pair_from_colorpair(
                comp_dict.get("background")
            ),
            button=self._init_color_pair_from_colorpair(comp_dict.get("button")),
            button_focused=self._init_color_pair_from_colorpair(
                comp_dict.get("button_focused")
            ),
            text_input=self._init_color_pair_from_colorpair(
                comp_dict.get("text_input")
            ),
            border=self._init_color_pair_from_colorpair(comp_dict.get("border")),
            selection=self._init_color_pair_from_colorpair(comp_dict.get("selection")),
            disabled=self._init_color_pair_from_colorpair(comp_dict.get("disabled")),
        )

        return semantic_colors, component_colors

    def _init_color_pair_from_colorpair(self, color_pair) -> int:
        """
        Initialize a curses color pair from a ColorPair object.

        Args:
            color_pair: ColorPair with foreground and background RGB tuples, or None

        Returns:
            Color pair number that can be used with curses.color_pair()
        """
        if color_pair is None:
            return 0
        return self.init_color_pair(color_pair.foreground, color_pair.background)

    def reset(self) -> None:
        """
        Reset color pair counter and cache.

        WARNING: This is a class-level operation that affects ALL ColorManager
        instances. It should only be used in testing environments.

        In production code, color pairs should persist for the lifetime of the
        curses session. Calling reset() will cause previously allocated pair
        numbers to be invalid, potentially breaking active themes.

        This method is primarily for pytest fixtures to ensure test isolation.
        """
        ColorManager._next_pair = 1
        ColorManager._pair_cache.clear()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ColorManager(colors={self.color_count})"
