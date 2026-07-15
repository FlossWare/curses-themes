#!/usr/bin/env python3
"""
3D theming support for curses applications.

This module extends the base Theme class with 3D rendering capabilities,
including shadow effects, highlight/lowlight edges, and raised/sunken borders.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import contextlib
import curses
from typing import Optional

from .theme import ColorPair, Theme, _calculate_display_width


class Theme3D(Theme):
    """
    Theme with 3D rendering capabilities (shadows, beveled edges).

    Extends Theme with shadow, highlight, and lowlight colors for 3D effects.
    There are three ways to provide 3D color data:

    1. Class attributes (declarative)::

        class My3DTheme(Theme3D):
            color_map = {...}
            effects_3d = {
                'shadow': ((0, 0, 0), (0, 0, 0)),
                'highlight': ((255, 255, 255), (200, 200, 200)),
                'lowlight': ((64, 64, 64), (200, 200, 200)),
            }

    2. Direct instantiation::

        theme = Theme3D(name="My 3D", color_map={...}, effects_3d={...})

    3. Method override::

        class My3DTheme(Theme3D):
            def get_3d_colors(self):
                return {'shadow': ColorPair(...), ...}
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        author: str = "",
        *,
        color_map=None,
        component_colors=None,
        border_chars=None,
        effects_3d: Optional[
            dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]
        ] = None,
        double_border_chars: Optional[str] = None,
    ):
        super().__init__(
            name,
            description,
            author,
            color_map=color_map,
            component_colors=component_colors,
            border_chars=border_chars,
        )
        self._shadow_offset_x = 2
        self._shadow_offset_y = 1
        self._shadow_color_pair: Optional[int] = None
        self._highlight_color_pair: Optional[int] = None
        self._lowlight_color_pair: Optional[int] = None
        self._effects_3d_data = effects_3d
        self._double_border_chars_data = double_border_chars

    @property
    def shadow_offset_x(self) -> int:
        return self._shadow_offset_x

    @shadow_offset_x.setter
    def shadow_offset_x(self, value: int) -> None:
        if value < 0:
            raise ValueError("Shadow offset must be non-negative")
        self._shadow_offset_x = value

    @property
    def shadow_offset_y(self) -> int:
        return self._shadow_offset_y

    @shadow_offset_y.setter
    def shadow_offset_y(self, value: int) -> None:
        if value < 0:
            raise ValueError("Shadow offset must be non-negative")
        self._shadow_offset_y = value

    def get_3d_colors(self) -> dict[str, ColorPair]:
        """
        Get 3D color pairs (shadow, highlight, lowlight).

        Resolution order: instance data -> class attribute ``effects_3d``
        -> raises NotImplementedError.
        """
        data = self._effects_3d_data
        if data is None:
            data = self.__class__.__dict__.get("effects_3d")
        if isinstance(data, dict) and data:
            return {name: ColorPair(fg, bg) for name, (fg, bg) in data.items()}
        raise NotImplementedError(
            f"Theme3D '{self.name}' must either set an effects_3d class attribute "
            f"or pass effects_3d to __init__()"
        )

    def get_double_border_chars(self) -> str:
        """Get double-line border characters for 3D boxes."""
        if self._double_border_chars_data is not None:
            return self._double_border_chars_data
        return self.__class__.__dict__.get("double_border_chars", "╔═╗║║╚═╝")

    def supports_3d(self) -> bool:
        return True

    def apply(self, stdscr) -> None:
        """Apply this theme including 3D color pairs."""
        super().apply(stdscr)

        from .colors import ColorManager

        color_manager = ColorManager(stdscr)

        colors_3d = self.get_3d_colors()
        for required in ("shadow", "highlight", "lowlight"):
            if required not in colors_3d:
                raise RuntimeError(
                    f"Theme3D '{self.name}' missing required 3D color: {required}"
                )

        self._shadow_color_pair = color_manager.init_color_pair(
            colors_3d["shadow"].foreground, colors_3d["shadow"].background
        )
        self._highlight_color_pair = color_manager.init_color_pair(
            colors_3d["highlight"].foreground, colors_3d["highlight"].background
        )
        self._lowlight_color_pair = color_manager.init_color_pair(
            colors_3d["lowlight"].foreground, colors_3d["lowlight"].background
        )

    @property
    def shadow_color_pair(self) -> int:
        if self._shadow_color_pair is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._shadow_color_pair

    @property
    def highlight_color_pair(self) -> int:
        if self._highlight_color_pair is None:
            raise RuntimeError(
                f"Theme '{self.name}' has not been applied. "
                "Call theme.apply(stdscr) first."
            )
        return self._highlight_color_pair

    @property
    def lowlight_color_pair(self) -> int:
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
        """Draw a 3D bordered box with beveled edges and drop shadow."""
        if height < 2 or width < 2:
            raise ValueError(
                f"Box dimensions too small: {height}x{width}. Minimum is 2x2."
            )

        border_chars = self.get_border_chars()
        if len(border_chars) != 8:
            raise ValueError(
                f"get_border_chars() must return 8 characters, got {len(border_chars)}"
            )

        top_left, top, top_right, left, right, bottom_left, bottom, bottom_right = (
            tuple(border_chars)
        )

        # Draw drop shadow
        if self.shadow_offset_x > 0 or self.shadow_offset_y > 0:
            shadow_attr = curses.color_pair(self.shadow_color_pair)
            shadow_y = y + self.shadow_offset_y
            shadow_x = x + self.shadow_offset_x

            if self.shadow_offset_x > 0:
                for i in range(height):
                    for j in range(self.shadow_offset_x):
                        with contextlib.suppress(curses.error):
                            window.addch(shadow_y + i, x + width + j, " ", shadow_attr)

            if self.shadow_offset_y > 0:
                for i in range(self.shadow_offset_y):
                    for j in range(width):
                        with contextlib.suppress(curses.error):
                            window.addch(y + height + i, shadow_x + j, " ", shadow_attr)

        # Draw main border
        border_attr = curses.color_pair(self.components.border)

        try:
            window.addstr(y, x, top_left, border_attr)
            window.addstr(y, x + width - 1, top_right, border_attr)
            window.addstr(y + height - 1, x, bottom_left, border_attr)
            window.addstr(y + height - 1, x + width - 1, bottom_right, border_attr)
        except curses.error:
            pass

        for i in range(1, width - 1):
            try:
                window.addstr(y, x + i, top, border_attr)
                window.addstr(y + height - 1, x + i, bottom, border_attr)
            except curses.error:
                pass

        for i in range(1, height - 1):
            try:
                window.addstr(y + i, x, left, border_attr)
                window.addstr(y + i, x + width - 1, right, border_attr)
            except curses.error:
                pass

        # Draw 3D beveled edges
        if height >= 4 and width >= 4:
            if raised:
                top_left_attr = curses.color_pair(self.highlight_color_pair)
                bottom_right_attr = curses.color_pair(self.lowlight_color_pair)
            else:
                top_left_attr = curses.color_pair(self.lowlight_color_pair)
                bottom_right_attr = curses.color_pair(self.highlight_color_pair)

            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + 1, x + i, " ", top_left_attr)

            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + 1, " ", top_left_attr)

            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + height - 2, x + i, " ", bottom_right_attr)

            for i in range(1, height - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + i, x + width - 2, " ", bottom_right_attr)
        elif height == 3 and width >= 3:
            if raised:
                attr = curses.color_pair(self.highlight_color_pair)
            else:
                attr = curses.color_pair(self.lowlight_color_pair)
            for i in range(1, width - 1):
                with contextlib.suppress(curses.error):
                    window.addch(y + 1, x + i, " ", attr)

        if title:
            title_display_width = _calculate_display_width(title)
            if width > title_display_width + 4:
                title_x = x + (width - title_display_width - 2) // 2
                with contextlib.suppress(curses.error):
                    window.addstr(y, title_x, f" {title} ", border_attr)

    def __repr__(self) -> str:
        return f"Theme3D(name='{self.name}', author='{self.author}')"
