import curses

import pytest

from curses_themes.menus import AcceleratorError, Menu, MenuItem, key_to_accelerator, normalize_accelerator


def test_normalize_accelerator_aliases_and_modifiers():
    assert normalize_accelerator(" Ctrl+S ") == "ctrl+s"
    assert normalize_accelerator("alt+F") == "alt+f"
    assert normalize_accelerator("return") == "enter"
    assert normalize_accelerator("esc") == "escape"


def test_duplicate_accelerators_are_rejected():
    with pytest.raises(AcceleratorError):
        Menu([MenuItem("One", accelerator="x"), MenuItem("Two", accelerator="x")])


def test_menu_accelerator_dispatches_action():
    called = []
    menu = Menu([
        MenuItem("Open", lambda: called.append("open"), accelerator="o"),
        MenuItem("Save", lambda: called.append("save"), accelerator="ctrl+s"),
    ])
    menu.handle_key(ord("o"))
    menu.handle_key(ord("s"), ctrl=True)
    assert called == ["open", "save"]
    assert menu.selected == 1


def test_menu_navigation_and_enter_activate_selected_item():
    called = []
    menu = Menu([
        MenuItem("One", lambda: called.append("one")),
        MenuItem("Two", lambda: called.append("two")),
    ])
    assert menu.selected == 0
    menu.handle_key(curses.KEY_DOWN)
    assert menu.selected == 1
    menu.handle_key(curses.KEY_ENTER)
    assert called == ["two"]


def test_disabled_accelerator_does_not_activate():
    called = []
    menu = Menu([MenuItem("Open", lambda: called.append("open"), accelerator="o", enabled=False)])
    menu.handle_key(ord("o"))
    assert called == []


def test_mouse_activation_selects_item():
    called = []
    menu = Menu([
        MenuItem("One", lambda: called.append("one")),
        MenuItem("Two", lambda: called.append("two")),
    ])
    clicked = getattr(curses, "BUTTON1_CLICKED", 0)
    if not clicked:
        pytest.skip("curses does not expose primary click events")
    assert menu.handle_mouse((6, 10, clicked), y=10, x=0) is None
    assert menu.selected == 1
    assert called == ["two"]


def test_key_to_accelerator_supports_modifiers():
    assert key_to_accelerator(ord("s"), ctrl=True) == "ctrl+s"
    assert key_to_accelerator(ord("f"), alt=True) == "alt+f"
    assert key_to_accelerator(27) == "escape"
