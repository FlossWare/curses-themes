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
        ColorManager instances.
    """

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

    _next_pair = 1
    _pair_cache: dict[tuple[int, int], int] = {}

    def __init__(self, stdscr):
        """Initialize color manager for a curses screen."""
        self.stdscr = stdscr
        if not curses.has_colors():
            raise RuntimeError(
                "Terminal does not support colors. Please use a color-capable terminal emulator."
            )
        curses.start_color()
        curses.use_default_colors()
        self.color_count = self._detect_color_capability()

    def _detect_color_capability(self) -> int:
        """Detect terminal color support level."""
        max_colors = curses.COLORS
        if max_colors >= 256:
            return 256
        elif max_colors >= 16:
            return 16
        else:
            return 8

    def _rgb_to_curses_color(self, r: int, g: int, b: int) -> int:
        """Convert RGB values to a curses color number."""
        if self.color_count >= 256:
            return self._rgb_to_256(r, g, b)
        return self._rgb_to_basic(r, g, b)

    def _rgb_to_256(self, r: int, g: int, b: int) -> int:
        """Map RGB to 256-color palette."""
        if r == g == b:
            if r < 4:
                return 16
            if r > 246:
                return 231
            return min(232 + (r - 3) // 10, 255)
        r_index = self._component_to_cube_index(r)
        g_index = self._component_to_cube_index(g)
        b_index = self._component_to_cube_index(b)
        return 16 + (36 * r_index) + (6 * g_index) + b_index

    @staticmethod
    def _component_to_cube_index(v: int) -> int:
        """Map a single RGB component to the xterm cube index."""
        if v < 48:
            return 0
        if v < 115:
            return 1
        return (v - 35) // 40

    def _rgb_to_basic(self, r: int, g: int, b: int) -> int:
        """Map RGB to 8 or 16 basic ANSI colors."""
        # curses color constants are not identical across implementations.
        # Build the palette from the active module instead of relying on values
        # captured when this module was imported.
        basic_colors = {
            curses.COLOR_BLACK: (0, 0, 0),
            curses.COLOR_RED: (205, 0, 0),
            curses.COLOR_GREEN: (0, 205, 0),
            curses.COLOR_YELLOW: (205, 205, 0),
            curses.COLOR_BLUE: (0, 0, 238),
            curses.COLOR_MAGENTA: (205, 0, 205),
            curses.COLOR_CYAN: (0, 205, 205),
            curses.COLOR_WHITE: (229, 229, 229),
        }
        min_distance = float("inf")
        closest_color = curses.COLOR_WHITE
        for color, (cr, cg, cb) in basic_colors.items():
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
        """Initialize a curses color pair from RGB values."""
        fg_color = self._rgb_to_curses_color(*fg_rgb)
        bg_color = -1 if bg_rgb is None else self._rgb_to_curses_color(*bg_rgb)
        cache_key = (fg_color, bg_color)
        if cache_key in ColorManager._pair_cache:
            return ColorManager._pair_cache[cache_key]
        pair_num = ColorManager._next_pair
        if pair_num >= curses.COLOR_PAIRS:
            raise RuntimeError(
                f"Exceeded maximum color pairs ({curses.COLOR_PAIRS}). Too many themes or colors in use."
            )
        try:
            curses.init_pair(pair_num, fg_color, bg_color)
        except curses.error as e:
            raise RuntimeError(
                f"Failed to initialize color pair {pair_num} (fg={fg_color}, bg={bg_color}): {e}"
            )
        ColorManager._next_pair += 1
        ColorManager._pair_cache[cache_key] = pair_num
        return pair_num

    def initialize_theme(self, theme) -> tuple[SemanticColors, ComponentColors]:
        """Initialize all color pairs for a theme."""
        color_map = theme.get_color_map()
        required_colors = {
            "background", "foreground", "primary", "success",
            "error", "warning", "info", "accent",
        }
        missing = required_colors - set(color_map.keys())
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(
                f"Theme '{theme.name}' is incomplete - missing required colors: {missing_list}\n"
                "get_color_map() must return all 8 required colors"
            )
        bg_rgb = color_map["background"]
        background_pair = self.init_color_pair(color_map["foreground"], bg_rgb)
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
        comp_dict = theme.get_components()
        component_colors = ComponentColors(
            background=self._init_color_pair_from_colorpair(comp_dict.get("background")),
            button=self._init_color_pair_from_colorpair(comp_dict.get("button")),
            button_focused=self._init_color_pair_from_colorpair(comp_dict.get("button_focused")),
            text_input=self._init_color_pair_from_colorpair(comp_dict.get("text_input")),
            border=self._init_color_pair_from_colorpair(comp_dict.get("border")),
            selection=self._init_color_pair_from_colorpair(comp_dict.get("selection")),
            disabled=self._init_color_pair_from_colorpair(comp_dict.get("disabled")),
        )
        return semantic_colors, component_colors

    def _init_color_pair_from_colorpair(self, color_pair) -> int:
        """Initialize a curses color pair from a ColorPair object."""
        if color_pair is None:
            return 0
        return self.init_color_pair(color_pair.foreground, color_pair.background)

    def reset(self) -> None:
        """Reset color pair counter and cache."""
        ColorManager._next_pair = 1
        ColorManager._pair_cache.clear()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ColorManager(colors={self.color_count})"
