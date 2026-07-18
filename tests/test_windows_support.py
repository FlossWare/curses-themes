"""Tests for Windows import error handling in __init__.py."""

import importlib
import sys
from unittest.mock import patch

import pytest


def _reload_curses_themes(platform: str, block_curses: bool):
    """Remove curses_themes from module cache and re-import it.

    If *block_curses* is True, make ``import curses`` raise ImportError so the
    try/except block in ``__init__.py`` is exercised.
    """
    mods_to_remove = [k for k in sys.modules if k.startswith("curses_themes")]
    saved_modules = {k: sys.modules.pop(k) for k in mods_to_remove}

    real_import = builtins_import()

    def guarded_import(name, *args, **kwargs):
        if block_curses and name in ("_curses", "curses"):
            raise ImportError(f"No module named '{name}'")
        return real_import(name, *args, **kwargs)

    try:
        with (
            patch.object(sys, "platform", platform),
            patch("builtins.__import__", side_effect=guarded_import),
        ):
            return importlib.import_module("curses_themes")
    finally:
        for k in list(sys.modules):
            if k.startswith("curses_themes"):
                del sys.modules[k]
        sys.modules.update(saved_modules)


def builtins_import():
    """Get the real __import__ regardless of builtins type."""
    import builtins
    return builtins.__import__


def test_windows_missing_curses_gives_helpful_message():
    """On Windows with no curses module, the error should mention windows-curses."""
    with pytest.raises(ImportError, match="windows-curses"):
        _reload_curses_themes("win32", block_curses=True)


def test_non_windows_reraises_original_error():
    """On non-Windows, a curses import error should re-raise unchanged."""
    with pytest.raises(ImportError, match="No module named"):
        _reload_curses_themes("linux", block_curses=True)


def test_non_windows_does_not_mention_windows_curses():
    """On non-Windows, the error should NOT mention windows-curses."""
    with pytest.raises(ImportError) as exc_info:
        _reload_curses_themes("linux", block_curses=True)
    assert "windows-curses" not in str(exc_info.value)
