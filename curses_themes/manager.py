#!/usr/bin/env python3
"""
Theme management and registration system.

This module provides the ThemeManager singleton for loading, registering,
and managing available themes.

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

from typing import Optional

from .theme import Theme


class ThemeManager:
    """
    Singleton manager for theme registration and loading.

    Provides a central registry for all available themes, including built-in
    themes and custom user themes. Themes are registered by name and can be
    loaded on demand.

    Example:
        ```python
        # Load a built-in theme
        theme = ThemeManager.load('dark')
        theme.apply(stdscr)

        # Register a custom theme
        ThemeManager.register(MyCustomTheme)
        theme = ThemeManager.load('my-custom-theme')

        # List all available themes
        for name, info in ThemeManager.list_themes().items():
            print(f"{name}: {info['description']}")
        ```

    Note:
        This is a singleton class. All methods are classmethods and operate
        on shared state. Do not instantiate this class.
    """

    # Registry of theme classes by normalized name
    _themes: dict[str, type[Theme]] = {}

    # Cache of theme metadata (name, description, author) by normalized name
    _theme_metadata: dict[str, dict[str, str]] = {}

    # Currently active theme instance
    _current_theme: Optional[Theme] = None

    # Flag to track if built-in themes have been registered
    _builtin_registered: bool = False

    def __init__(self):
        """
        Prevent instantiation of singleton.

        Raises:
            TypeError: Always - this class should not be instantiated
        """
        raise TypeError(
            "ThemeManager is a singleton and should not be instantiated. "
            "Use ThemeManager.load(), ThemeManager.register(), etc."
        )

    @classmethod
    def _normalize_name(cls, name: str) -> str:
        """
        Normalize theme name for consistent lookup.

        Converts to lowercase and replaces spaces/underscores with hyphens.

        Args:
            name: Theme name to normalize

        Returns:
            Normalized theme name
        """
        return name.lower().replace(" ", "-").replace("_", "-")

    @classmethod
    def _register_builtin_themes(cls) -> None:
        """
        Register all built-in themes.

        This is called automatically on first use of load() or list_themes().
        Built-in themes are lazily loaded from the themes package.
        """
        if cls._builtin_registered:
            return

        # Import built-in themes
        # This is done lazily to avoid circular imports and to defer
        # loading themes until they're actually needed
        try:
            from .themes.borland3d import Borland3DTheme
            from .themes.dark import DarkTheme
            from .themes.dbase3 import DBase3Theme
            from .themes.dbase4 import DBase4Theme
            from .themes.dbase4_3d import DBase4_3DTheme
            from .themes.default import DefaultTheme
            from .themes.dos import DOSTheme
            from .themes.light import LightTheme
            from .themes.ti994a import TI994ATheme
            from .themes.trs80 import TRS80Theme
        except ImportError:
            pass
        else:
            cls.register(DefaultTheme, "default")
            cls.register(DarkTheme, "dark")
            cls.register(LightTheme, "light")
            cls.register(TI994ATheme, "ti-99-4a")
            cls.register(TRS80Theme, "trs-80")
            cls.register(DOSTheme, "dos")
            cls.register(DBase3Theme, "dbase-iii")
            cls.register(DBase4Theme, "dbase-iv")
            cls.register(Borland3DTheme, "borland-3d")
            cls.register(DBase4_3DTheme, "dbase-iv-3d")

        cls._builtin_registered = True

    @classmethod
    def register(cls, theme_class: type[Theme], name: Optional[str] = None) -> None:
        """
        Register a theme class for use.

        Args:
            theme_class: Theme class (subclass of Theme) to register
            name: Optional custom name. If not provided, uses theme.name
                 from a temporary instance.

        Raises:
            TypeError: If theme_class is not a Theme subclass
            ValueError: If a theme with this name is already registered

        Example:
            ```python
            class MyTheme(Theme):
                def __init__(self):
                    super().__init__("My Theme", "A custom theme")

                def get_color_map(self):
                    return {...}

            # Register with automatic name
            ThemeManager.register(MyTheme)

            # Or register with custom name
            ThemeManager.register(MyTheme, 'my-custom')
            ```
        """
        if not isinstance(theme_class, type):
            raise TypeError(
                f"Expected a Theme class, got an instance of {type(theme_class).__name__}. "
                "Pass the class itself, not an instance: "
                f"ThemeManager.register({type(theme_class).__name__})"
            )

        if not issubclass(theme_class, Theme):
            raise TypeError(
                f"{theme_class.__name__} is not a Theme subclass. "
                "All themes must inherit from Theme."
            )

        # Get name from theme instance if not provided
        if name is None:
            temp_instance = theme_class()  # type: ignore[call-arg]
            name = temp_instance.name
            # Cache metadata while we have the instance
            cls._theme_metadata[cls._normalize_name(name)] = {
                "name": temp_instance.name,
                "description": temp_instance.description,
                "author": temp_instance.author,
            }
        else:
            # When explicit name is provided, we still need to cache metadata
            # Create temporary instance only if not already cached
            normalized_name = cls._normalize_name(name)
            if normalized_name not in cls._theme_metadata:
                temp_instance = theme_class()  # type: ignore[call-arg]
                cls._theme_metadata[normalized_name] = {
                    "name": temp_instance.name,
                    "description": temp_instance.description,
                    "author": temp_instance.author,
                }

        normalized_name = cls._normalize_name(name)

        # Check for conflicts
        if normalized_name in cls._themes:
            existing = cls._themes[normalized_name]
            if existing != theme_class:
                raise ValueError(
                    f"Theme '{normalized_name}' is already registered "
                    f"({existing.__name__}). Use a different name or "
                    f"unregister the existing theme first."
                )
            # Same class already registered, silently ignore
            return

        cls._themes[normalized_name] = theme_class

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Unregister a theme by name.

        Args:
            name: Name of theme to unregister

        Raises:
            KeyError: If theme is not registered

        Example:
            ```python
            ThemeManager.unregister('my-custom-theme')
            ```
        """
        normalized_name = cls._normalize_name(name)

        if normalized_name not in cls._themes:
            raise KeyError(
                f"Theme '{normalized_name}' is not registered. "
                f"Available themes: {', '.join(cls._themes.keys())}"
            )

        # Get the theme class before deletion
        theme_class = cls._themes[normalized_name]
        del cls._themes[normalized_name]

        # Also remove cached metadata
        if normalized_name in cls._theme_metadata:
            del cls._theme_metadata[normalized_name]

        # Clear current theme if it was an instance of the unregistered theme
        if cls._current_theme and isinstance(cls._current_theme, theme_class):
            cls._current_theme = None

    @classmethod
    def load(cls, name: str) -> Theme:
        """
        Load a theme by name.

        Creates a new instance of the requested theme. Built-in themes are
        automatically registered on first load.

        Args:
            name: Theme name (case-insensitive, spaces/underscores converted to hyphens)

        Returns:
            New Theme instance

        Raises:
            KeyError: If theme is not registered

        Example:
            ```python
            theme = ThemeManager.load('dark')
            theme.apply(stdscr)

            # Names are normalized
            theme = ThemeManager.load('Dark')  # Same as 'dark'
            theme = ThemeManager.load('my_custom_theme')  # Same as 'my-custom-theme'
            ```
        """
        # Ensure built-in themes are registered
        cls._register_builtin_themes()

        normalized_name = cls._normalize_name(name)

        if normalized_name not in cls._themes:
            available = ", ".join(sorted(cls._themes.keys()))
            raise KeyError(
                f"Theme '{normalized_name}' not found. Available themes: {available}"
            )

        # Create new instance
        theme_class = cls._themes[normalized_name]
        theme_instance = theme_class()  # type: ignore[call-arg]

        # Track as current theme
        cls._current_theme = theme_instance

        return theme_instance

    @classmethod
    def list_themes(cls) -> dict[str, dict[str, str]]:
        """
        List all registered themes with metadata.

        Returns:
            Dictionary mapping theme names to metadata dictionaries with
            keys: 'name', 'description', 'author'

        Example:
            ```python
            themes = ThemeManager.list_themes()
            for name, info in themes.items():
                print(f"{name}:")
                print(f"  Name: {info['name']}")
                print(f"  Description: {info['description']}")
                print(f"  Author: {info['author']}")
            ```
        """
        # Ensure built-in themes are registered
        cls._register_builtin_themes()

        result = {}
        for normalized_name in sorted(cls._themes.keys()):
            # Use cached metadata if available
            if normalized_name in cls._theme_metadata:
                result[normalized_name] = cls._theme_metadata[normalized_name].copy()
            else:
                # Fallback: create temp instance if metadata wasn't cached
                # This should rarely happen (only for themes registered before this optimization)
                theme_class = cls._themes[normalized_name]
                temp_instance = theme_class()  # type: ignore[call-arg]
                metadata = {
                    "name": temp_instance.name,
                    "description": temp_instance.description,
                    "author": temp_instance.author,
                }
                # Cache it for next time
                cls._theme_metadata[normalized_name] = metadata
                result[normalized_name] = metadata.copy()

        return result

    @classmethod
    def get_current(cls) -> Optional[Theme]:
        """
        Get the currently active theme.

        Returns:
            Current Theme instance, or None if no theme has been loaded

        Example:
            ```python
            current = ThemeManager.get_current()
            if current:
                print(f"Current theme: {current.name}")
            ```
        """
        return cls._current_theme

    @classmethod
    def reset(cls) -> None:
        """
        Reset the theme manager state.

        Clears all registered themes and current theme. This is primarily
        for testing purposes.

        Warning:
            This will unregister all themes, including built-in themes.
            They will be re-registered on next load() or list_themes() call.
        """
        cls._themes.clear()
        cls._theme_metadata.clear()
        cls._current_theme = None
        cls._builtin_registered = False

    @classmethod
    def __repr__(cls) -> str:
        """String representation for debugging."""
        theme_count = len(cls._themes)
        current = cls._current_theme.name if cls._current_theme else "None"
        return f"ThemeManager(themes={theme_count}, current='{current}')"
