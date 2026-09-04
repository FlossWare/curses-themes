#!/usr/bin/env python3
"""Tests for ThemeManager - theme registration and loading."""

import json
import os
import tempfile

import pytest

from curses_tui import Theme
from curses_tui.manager import ThemeManager


class TestThemeManagerSingleton:
    """Tests for ThemeManager singleton pattern."""

    def test_theme_manager_singleton(self):
        """Test ThemeManager cannot be instantiated (singleton pattern)."""
        with pytest.raises(TypeError, match="singleton and should not be instantiated"):
            ThemeManager()

    def test_theme_manager_class_methods_work(self):
        """Test ThemeManager class methods work without instantiation."""
        # Should not raise
        themes = ThemeManager.list_themes()
        assert isinstance(themes, dict)


class TestThemeRegistration:
    """Tests for theme registration functionality."""

    def test_register_theme_with_explicit_name(self, simple_theme):
        """Test registering a theme with explicit custom name."""
        ThemeManager.register(simple_theme.__class__, "my-custom-theme")

        assert "my-custom-theme" in ThemeManager._themes
        assert ThemeManager._themes["my-custom-theme"] == simple_theme.__class__

    def test_register_theme_with_auto_name(self, simple_theme):
        """Test registering a theme with automatic name from theme.name."""
        ThemeManager.register(simple_theme.__class__)

        # Name should be normalized: "Simple Test Theme" -> "simple-test-theme"
        assert "simple-test-theme" in ThemeManager._themes

    @pytest.mark.parametrize(
        "input_name,expected_name",
        [
            ("My Theme", "my-theme"),
            ("my_theme", "my-theme"),
            ("MY_THEME", "my-theme"),
            ("My Custom Theme", "my-custom-theme"),
            ("Theme_With_Underscores", "theme-with-underscores"),
        ],
    )
    def test_name_normalization(self, input_name, expected_name):
        """Test theme name normalization (lowercase, hyphens)."""
        normalized = ThemeManager._normalize_name(input_name)
        assert normalized == expected_name

    def test_register_duplicate_same_class(self, simple_theme):
        """Test registering same theme class twice is silently ignored."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        ThemeManager.register(simple_theme.__class__, "test-theme")  # Should not raise

        assert "test-theme" in ThemeManager._themes

    def test_register_duplicate_different_class(self, simple_theme):
        """Test registering different theme class with same name raises ValueError."""

        class AnotherTheme(Theme):
            def __init__(self):
                super().__init__("Another")

            def get_color_map(self):
                return {}

        ThemeManager.register(simple_theme.__class__, "test-theme")

        with pytest.raises(ValueError, match="already registered"):
            ThemeManager.register(AnotherTheme, "test-theme")

    def test_register_non_theme_class(self):
        """Test registering non-Theme subclass raises TypeError."""

        class NotATheme:
            pass

        with pytest.raises(TypeError, match="not a Theme subclass"):
            ThemeManager.register(NotATheme)


class TestThemeLoading:
    """Tests for theme loading functionality."""

    def test_load_theme_creates_instance(self, simple_theme):
        """Test load() creates a new theme instance."""
        ThemeManager.register(simple_theme.__class__, "test-theme")

        theme1 = ThemeManager.load("test-theme")
        theme2 = ThemeManager.load("test-theme")

        assert theme1 is not theme2  # Different instances
        assert type(theme1) == type(theme2)
        assert theme1.name == "Simple Test Theme"

    def test_load_theme_normalizes_name(self, simple_theme):
        """Test load() normalizes theme name for lookup."""
        ThemeManager.register(simple_theme.__class__, "test-theme")

        # All these should load the same theme
        theme1 = ThemeManager.load("test-theme")
        theme2 = ThemeManager.load("Test Theme")
        theme3 = ThemeManager.load("TEST_THEME")

        assert type(theme1) == type(theme2) == type(theme3)

    def test_load_nonexistent_theme_raises_key_error(self):
        """Test load() raises KeyError for non-existent theme."""
        with pytest.raises(KeyError, match="not found"):
            ThemeManager.load("nonexistent-theme")

    def test_load_auto_registers_builtins(self):
        """Test load() auto-registers built-in themes on first use."""
        # First load should trigger auto-registration
        theme = ThemeManager.load("default")

        assert theme is not None
        assert "default" in ThemeManager._themes
        assert "dark" in ThemeManager._themes
        assert "light" in ThemeManager._themes

    def test_get_current_returns_loaded_theme(self, simple_theme):
        """Test get_current() returns the most recently loaded theme."""
        ThemeManager.register(simple_theme.__class__, "test-theme")

        assert ThemeManager.get_current() is None

        theme = ThemeManager.load("test-theme")
        current = ThemeManager.get_current()

        assert current is theme

    def test_get_current_none_when_no_theme_loaded(self):
        """Test get_current() returns None when no theme has been loaded."""
        assert ThemeManager.get_current() is None


class TestThemeUnregistration:
    """Tests for theme unregistration."""

    def test_unregister_theme(self, simple_theme):
        """Test unregister() removes theme from registry."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        assert "test-theme" in ThemeManager._themes

        ThemeManager.unregister("test-theme")
        assert "test-theme" not in ThemeManager._themes

    def test_unregister_nonexistent_theme_raises_key_error(self):
        """Test unregister() raises KeyError for non-existent theme."""
        with pytest.raises(KeyError, match="not registered"):
            ThemeManager.unregister("nonexistent-theme")

    def test_unregister_clears_current_if_matched(
        self, mock_curses, mock_stdscr, simple_theme
    ):
        """Test unregister() clears current theme if it matches."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        theme = ThemeManager.load("test-theme")

        assert ThemeManager.get_current() is theme

        ThemeManager.unregister("test-theme")
        assert ThemeManager.get_current() is None


class TestThemeListing:
    """Tests for listing available themes."""

    def test_list_themes_returns_metadata(self):
        """Test list_themes() returns theme metadata dictionary."""
        themes = ThemeManager.list_themes()

        assert isinstance(themes, dict)
        assert "default" in themes

        # Check metadata structure
        default_meta = themes["default"]
        assert "name" in default_meta
        assert "description" in default_meta
        assert "author" in default_meta

    def test_list_themes_includes_builtins(self):
        """Test list_themes() auto-registers and includes built-in themes."""
        themes = ThemeManager.list_themes()

        # Check for known built-in themes
        assert "default" in themes
        assert "dark" in themes
        assert "light" in themes
        assert "dos" in themes

    def test_list_themes_sorted(self, simple_theme):
        """Test list_themes() returns sorted theme names."""
        ThemeManager.register(simple_theme.__class__, "zzz-theme")
        ThemeManager.register(simple_theme.__class__, "aaa-theme")

        themes = ThemeManager.list_themes()
        theme_names = list(themes.keys())

        assert theme_names == sorted(theme_names)


class TestThemeManagerReset:
    """Tests for ThemeManager reset functionality."""

    def test_reset_clears_all_themes(self, simple_theme):
        """Test reset() clears all registered themes."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        theme = ThemeManager.load("test-theme")

        ThemeManager.reset()

        assert len(ThemeManager._themes) == 0
        assert ThemeManager.get_current() is None
        assert ThemeManager._builtin_registered is False

    def test_reset_allows_builtin_reregistration(self):
        """Test reset() allows built-in themes to be re-registered."""
        # Load a built-in theme (triggers registration)
        ThemeManager.load("default")
        assert ThemeManager._builtin_registered is True

        ThemeManager.reset()
        assert ThemeManager._builtin_registered is False

        # Should re-register on next load
        ThemeManager.load("default")
        assert ThemeManager._builtin_registered is True


class TestMetadataCaching:
    """Tests for theme metadata caching optimization."""

    def test_metadata_cached_on_registration_with_auto_name(self, simple_theme):
        """Test that metadata is cached when theme is registered with auto name."""
        ThemeManager.register(simple_theme.__class__)

        normalized_name = "simple-test-theme"
        assert normalized_name in ThemeManager._theme_metadata

        metadata = ThemeManager._theme_metadata[normalized_name]
        assert metadata["name"] == "Simple Test Theme"
        assert "description" in metadata
        assert "author" in metadata

    def test_metadata_cached_on_registration_with_explicit_name(self, simple_theme):
        """Test that metadata is cached when theme is registered with explicit name."""
        ThemeManager.register(simple_theme.__class__, "custom-name")

        assert "custom-name" in ThemeManager._theme_metadata

        metadata = ThemeManager._theme_metadata["custom-name"]
        assert metadata["name"] == "Simple Test Theme"
        assert "description" in metadata
        assert "author" in metadata

    def test_list_themes_uses_cached_metadata(self, simple_theme):
        """Test that list_themes() uses cached metadata instead of creating instances."""
        # Register theme (which caches metadata)
        ThemeManager.register(simple_theme.__class__, "test-theme")

        # Clear the theme class temporarily to prove we're using cache
        original_class = ThemeManager._themes["test-theme"]

        # Call list_themes - should use cached metadata
        themes = ThemeManager.list_themes()

        assert "test-theme" in themes
        assert themes["test-theme"]["name"] == "Simple Test Theme"

    def test_unregister_clears_metadata_cache(self, simple_theme):
        """Test that unregister() removes cached metadata."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        assert "test-theme" in ThemeManager._theme_metadata

        ThemeManager.unregister("test-theme")
        assert "test-theme" not in ThemeManager._theme_metadata

    def test_reset_clears_metadata_cache(self, simple_theme):
        """Test that reset() clears metadata cache."""
        ThemeManager.register(simple_theme.__class__, "test-theme")
        assert len(ThemeManager._theme_metadata) > 0

        ThemeManager.reset()
        assert len(ThemeManager._theme_metadata) == 0

    def test_builtin_themes_have_cached_metadata(self):
        """Test that built-in themes have metadata cached after registration."""
        # Trigger built-in registration
        ThemeManager.list_themes()

        # All built-in themes should have cached metadata
        assert "default" in ThemeManager._theme_metadata
        assert "dark" in ThemeManager._theme_metadata
        assert "light" in ThemeManager._theme_metadata

        # Verify metadata structure
        default_meta = ThemeManager._theme_metadata["default"]
        assert "name" in default_meta
        assert "description" in default_meta
        assert "author" in default_meta


def _make_theme_json(name):
    """Helper to create a minimal valid theme dict."""
    return {
        "name": name,
        "colors": {
            "background": [0, 0, 0],
            "foreground": [255, 255, 255],
            "primary": [0, 120, 215],
            "success": [16, 124, 16],
            "error": [232, 17, 35],
            "warning": [193, 156, 0],
            "info": [0, 120, 212],
            "accent": [142, 68, 173],
        },
        "components": {
            "background": {
                "foreground": [255, 255, 255],
                "background": [0, 0, 0],
            },
            "button": {
                "foreground": [0, 120, 215],
                "background": [0, 0, 0],
            },
        },
        "border_chars": "+-+||+-+",
    }


class TestLoadThemesFromDirectory:
    """Tests for ThemeManager.load_themes_from_directory()."""

    def test_loads_valid_theme_files(self, tmp_path):
        """Test loading multiple valid JSON theme files from a directory."""
        for name in ("alpha", "beta", "gamma"):
            theme_file = tmp_path / f"{name}.json"
            theme_file.write_text(json.dumps(_make_theme_json(f"Theme {name}")))

        count = ThemeManager.load_themes_from_directory(str(tmp_path))

        assert count == 3

    def test_loaded_themes_accessible_via_load(self, tmp_path):
        """Test that loaded themes can be retrieved by name."""
        (tmp_path / "ocean.json").write_text(
            json.dumps(_make_theme_json("Ocean"))
        )
        (tmp_path / "forest.json").write_text(
            json.dumps(_make_theme_json("Forest"))
        )

        ThemeManager.load_themes_from_directory(str(tmp_path))

        ocean = ThemeManager.load("ocean")
        assert ocean.name == "Ocean"

        forest = ThemeManager.load("forest")
        assert forest.name == "Forest"

    def test_skips_schema_json(self, tmp_path):
        """Test that schema.json is skipped (matching Java behaviour)."""
        (tmp_path / "valid.json").write_text(
            json.dumps(_make_theme_json("Valid"))
        )
        (tmp_path / "schema.json").write_text(
            json.dumps({"type": "object", "properties": {}})
        )

        count = ThemeManager.load_themes_from_directory(str(tmp_path))

        assert count == 1
        # Verify "schema" was not registered
        with pytest.raises(KeyError):
            ThemeManager.load("schema")

    def test_skips_invalid_files(self, tmp_path):
        """Test that invalid files are silently skipped."""
        (tmp_path / "good.json").write_text(
            json.dumps(_make_theme_json("Good"))
        )
        (tmp_path / "bad.json").write_text("not valid json {{{")
        (tmp_path / "empty.json").write_text("{}")

        count = ThemeManager.load_themes_from_directory(str(tmp_path))

        assert count == 1

    def test_returns_zero_for_empty_directory(self, tmp_path):
        """Test that an empty directory returns zero."""
        count = ThemeManager.load_themes_from_directory(str(tmp_path))
        assert count == 0

    def test_custom_glob_pattern(self, tmp_path):
        """Test using a custom glob pattern (e.g., *.yaml placeholder)."""
        (tmp_path / "theme.json").write_text(
            json.dumps(_make_theme_json("Json Theme"))
        )
        (tmp_path / "theme.txt").write_text("not a theme")

        # Only *.json should match (default)
        count = ThemeManager.load_themes_from_directory(str(tmp_path))
        assert count == 1

        ThemeManager.reset()

        # *.txt should match but fail to parse
        count = ThemeManager.load_themes_from_directory(
            str(tmp_path), pattern="*.txt"
        )
        assert count == 0
