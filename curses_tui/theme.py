#!/usr/bin/env python3
"""
Theme base classes and semantic color support for curses applications.

This module provides the core Theme class and SemanticColors container
that enable pluggable theming for Python curses applications.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import contextlib
import curses
import unicodedata
from typing import Optional


def _calculate_display_width(text: str) -> int:
    """Calculate the display width of text accounting for CJK characters."""
    width = 0
    for char in text:
        ea_width = unicodedata.east_asian_width(char)
        if ea_width in ("F", "W"):
            width += 2
        else:
            width += 1
    return width


class ColorPair:
    """Represents a foreground/background color pair."""

    def __init__(
        self, foreground: tuple[int, int, int], background: tuple[int, int, int]
    ):
        self.foreground = foreground
        self.background = background

    def __repr__(self):
        return f"ColorPair(fg={self.foreground}, bg={self.background})"


class ComponentColors:
    """
    Container for component-based color pairs used by themes.

    Attributes:
        background: Normal background color pair
        button: Button in normal state
        button_focused: Button when focused
        text_input: Text input fields
        border: Borders and frames
        selection: Selected/highlighted items
        disabled: Disabled components
    """

    def __init__(
        self,
        background: int,
        button: int,
        button_focused: int,
        text_input: int,
        border: int,
        selection: int,
        disabled: int,
    ):
        self.background = background
        self.button = button
        self.button_focused = button_focused
        self.text_input = text_input
        self.border = border
        self.selection = selection
        self.disabled = disabled

    def __repr__(self) -> str:
        return (
            f"ComponentColors(background={self.background}, button={self.button}, "
            f"button_focused={self.button_focused}, text_input={self.text_input}, "
            f"border={self.border}, selection={self.selection}, disabled={self.disabled})"
        )


class SemanticColors:
    """
    Container for semantic color pairs used by themes.

    Attributes:
        primary: Main UI color for highlights and focus
        success: Positive feedback and successful operations
        error: Error messages and critical warnings
        warning: Caution messages and non-critical warnings
        info: Informational messages and help text
        background: Default background color
        foreground: Default text color
        accent: Secondary highlight color
    """

    def __init__(
        self,
        primary: int,
        success: int,
        error: int,
        warning: int,
        info: int,
        background: int,
        foreground: int,
        accent: int,
    ):
        self.primary = primary
        self.success = success
        self.error = error
        self.warning = warning
        self.info = info
        self.background = background
        self.foreground = foreground
        self.accent = accent

    def __repr__(self) -> str:
        return (
            f"SemanticColors(primary={self.primary}, success={self.success}, "
            f"error={self.error}, warning={self.warning}, info={self.info}, "
            f"background={self.background}, foreground={self.foreground}, "
            f"accent={self.accent})"
        )


class Theme:
    """
    Base class for curses themes.

    Themes define the visual appearance of a curses application by mapping
    semantic colors to RGB values. There are three ways to define a theme:

    1. Class attributes (declarative)::

        class MyTheme(Theme):
            color_map = {
                'background': (0, 0, 0), 'foreground': (255, 255, 255),
                'primary': (0, 120, 215), 'success': (16, 124, 16),
                'error': (232, 17, 35), 'warning': (193, 156, 0),
                'info': (0, 120, 212), 'accent': (142, 68, 173),
            }
            component_colors = {
                'button': ((0, 120, 215), (0, 0, 0)),
            }

            def __init__(self):
                super().__init__(name="My Theme")

    2. Direct instantiation (no subclass needed)::

        theme = Theme(name="My Theme", color_map={...}, component_colors={...})

    3. Method overrides (for dynamic behavior)::

        class MyTheme(Theme):
            def get_color_map(self):
                return {...}

    Attributes:
        name: Human-readable theme name
        description: Brief description of the theme
        author: Theme creator's name
        colors: SemanticColors instance (available after apply())
        components: ComponentColors instance (available after apply())
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        author: str = "",
        *,
        color_map: Optional[dict[str, tuple[int, int, int]]] = None,
        component_colors: Optional[
            dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]
        ] = None,
        border_chars: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.author = author
        self._colors: Optional[SemanticColors] = None
        self._components: Optional[ComponentColors] = None
        self._color_map_data = color_map
        self._component_colors_data = component_colors
        self._border_chars_data = border_chars

    def get_color_map(self) -> dict[str, tuple[int, int, int]]:
        """
        Get RGB color definitions for this theme.

        Returns a dictionary mapping semantic color names to RGB tuples.
        Required keys: background, foreground, primary, success, error,
        warning, info, accent.

        Resolution order: instance data (from __init__) -> class attribute
        ``color_map`` -> raises NotImplementedError.
        """
        if self._color_map_data is not None:
            return dict(self._color_map_data)
        cls_attr = self.__class__.__dict__.get("color_map")
        if isinstance(cls_attr, dict):
            return dict(cls_attr)
        raise NotImplementedError(
            f"Theme '{self.name}' must either set a color_map class attribute "
            f"or pass color_map to __init__()"
        )

    def get_components(self) -> dict[str, ColorPair]:
        """
        Get component color pairs for this theme.

        Returns a dict mapping component names to ColorPair instances.
        Valid keys: background, button, button_focused, text_input,
        border, selection, disabled. Missing keys default to color pair 0.

        Resolution order: instance data (from __init__) -> class attribute
        ``component_colors`` -> empty dict (all defaults).
        """
        data = self._component_colors_data
        if data is None:
            data = self.__class__.__dict__.get("component_colors")
        if isinstance(data, dict) and data:
            return {name: ColorPair(fg, bg) for name, (fg, bg) in data.items()}
        return {}

    def get_border_chars(self) -> str:
        """
        Get border characters for drawing boxes.

        Returns a string with 8 characters: top-left, top, top-right,
        left, right, bottom-left, bottom, bottom-right.

        Resolution order: instance data -> class attribute ``border_chars``
        -> default ``"+-+||+-+"``.
        """
        if self._border_chars_data is not None:
            return self._border_chars_data
        return self.__class__.__dict__.get("border_chars", "+-+||+-+")

    def _validate_stdscr(self, stdscr, operation: str) -> None:
        """Validate stdscr is alive and usable."""
        try:
            stdscr.getmaxyx()
        except (AttributeError, curses.error) as e:
            raise RuntimeError(
                f"Cannot {operation} - curses window is no longer valid.\n"
                f"Ensure theme operations happen within the curses.wrapper() callback.\n"
                f"Original error: {e}"
            )

    def apply(self, stdscr) -> None:
        """
        Apply this theme to a curses screen.

        Initializes color pairs and sets up the theme for use. Must be called
        before using theme.colors, theme.components, or theme.draw_box().

        Args:
            stdscr: Curses window object (typically from curses.wrapper)
        """
        from .colors import ColorManager

        self._validate_stdscr(stdscr, "apply theme")

        color_manager = ColorManager(stdscr)
        self._colors, self._components = color_manager.initialize_theme(self)

        stdscr.bkgd(" ", curses.color_pair(self._components.background))

    @property
    def colors(self) -> SemanticColors:
        """
        Get semantic color pairs for this theme.

        Returns:
            SemanticColors instance with initialized color pair numbers.

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._colors is None:
            raise RuntimeError(
                f"Theme '{self.name}' colors not available - apply() must be called first.\n"
                f"Correct usage:\n"
                f"  theme = ThemeManager.load('{self.name.lower()}')\n"
                f"  theme.apply(stdscr)  # Initialize colors\n"
                f"  stdscr.addstr(0, 0, 'text', curses.color_pair(theme.colors.primary))"
            )
        return self._colors

    @property
    def components(self) -> ComponentColors:
        """
        Get component-based color pairs for this theme.

        Returns:
            ComponentColors instance with initialized color pair numbers.

        Raises:
            RuntimeError: If apply() has not been called yet
        """
        if self._components is None:
            raise RuntimeError(
                f"Theme '{self.name}' components not available - apply() must be called first.\n"
                f"Correct usage:\n"
                f"  theme = ThemeManager.load('{self.name.lower()}')\n"
                f"  theme.apply(stdscr)  # Initialize components\n"
                f"  stdscr.addstr(0, 0, 'Button', curses.color_pair(theme.components.button))"
            )
        return self._components

    def draw_box(
        self,
        window,
        y: int,
        x: int,
        height: int,
        width: int,
        title: str = "",
        color_pair: Optional[int] = None,
    ) -> None:
        """
        Draw a themed border box on the given window.

        Args:
            window: Curses window to draw on
            y: Top-left Y coordinate
            x: Top-left X coordinate
            height: Box height in characters
            width: Box width in characters
            title: Optional title to display centered in top border
            color_pair: Color pair number to use (defaults to border color)
        """
        self._validate_stdscr(window, "draw box")

        if height < 2 or width < 2:
            raise ValueError(
                f"Box dimensions too small: {height}x{width}. Minimum is 2x2."
            )

        if color_pair is None:
            color_pair = self.components.border

        border_chars = self.get_border_chars()
        if len(border_chars) != 8:
            raise ValueError(
                f"get_border_chars() must return 8 characters, got {len(border_chars)}"
            )

        top_left, top, top_right, left, right, bottom_left, bottom, bottom_right = (
            tuple(border_chars)
        )

        attr = curses.color_pair(color_pair)

        try:
            window.addstr(y, x, top_left, attr)
            window.addstr(y, x + width - 1, top_right, attr)
            window.addstr(y + height - 1, x, bottom_left, attr)
            window.addstr(y + height - 1, x + width - 1, bottom_right, attr)
        except curses.error:
            pass

        for i in range(1, width - 1):
            try:
                window.addstr(y, x + i, top, attr)
                window.addstr(y + height - 1, x + i, bottom, attr)
            except curses.error:
                pass

        for i in range(1, height - 1):
            try:
                window.addstr(y + i, x, left, attr)
                window.addstr(y + i, x + width - 1, right, attr)
            except curses.error:
                pass

        if title:
            title_display_width = _calculate_display_width(title)
            if width > title_display_width + 4:
                title_x = x + (width - title_display_width - 2) // 2
                with contextlib.suppress(curses.error):
                    window.addstr(y, title_x, f" {title} ", attr)

    def __repr__(self) -> str:
        return f"Theme(name='{self.name}', author='{self.author}')"
