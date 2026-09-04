import curses
from unittest.mock import patch

from curses_tui.input import (
    enable_mouse,
    is_cancel,
    is_confirm,
    is_down,
    is_mouse,
    is_primary_click,
    is_up,
    list_index_at,
    mouse_event,
    mouse_position,
    primary_click,
    resolve_list_mouse,
)


def test_list_index_at_is_scroll_aware_and_bounded():
    assert list_index_at(10, 10, 20) == 0
    assert list_index_at(12, 10, 20, scroll_offset=5, visible=4) == 7
    assert list_index_at(14, 10, 20, scroll_offset=5, visible=4) is None
    assert list_index_at(9, 10, 20) is None


def test_resolve_list_mouse_activates_primary_press_or_click():
    pressed = getattr(curses, "BUTTON1_PRESSED", 0)
    clicked = getattr(curses, "BUTTON1_CLICKED", 0)
    if pressed:
        assert resolve_list_mouse((4, 7, pressed), origin_y=5, count=10) == ("activate", 2)
    if clicked:
        assert resolve_list_mouse((4, 8, clicked), origin_y=5, count=10) == ("activate", 3)


def test_resolve_list_mouse_focuses_non_primary_event_and_rejects_outside():
    motion = getattr(curses, "REPORT_MOUSE_POSITION", 0)
    assert resolve_list_mouse((4, 7, motion), origin_y=5, count=10) == ("focus", 2)
    assert resolve_list_mouse((4, 20, motion), origin_y=5, count=10) is None


def test_mouse_event_normalizes_getmouse():
    with patch.object(curses, "getmouse", return_value=(1, 12, 8, 0, 123)):
        assert mouse_event() == (12, 8, 123)
        with patch.object(curses, "getmouse", return_value=(1, 12, 8, 0, 123)):
            assert mouse_position() == (12, 8)


def test_primary_click_reads_current_event():
    clicked = getattr(curses, "BUTTON1_CLICKED", 0)
    with patch("curses_tui.input.mouse_event", return_value=(3, 4, clicked)):
        assert primary_click() == (3, 4) if clicked else primary_click() is None


def test_enable_mouse_gracefully_handles_supported_and_unsupported_terminals():
    with patch.object(curses, "mousemask", return_value=(1, 0)) as mousemask:
        assert enable_mouse() is True
        mousemask.assert_called_once()
    with patch.object(curses, "mousemask", return_value=(0, 0)):
        assert enable_mouse() is False


def test_keyboard_helpers_remain_compatible():
    assert is_confirm(10)
    assert is_confirm(13)
    assert is_cancel(27)
    assert is_cancel(ord("q"))
    assert is_up(curses.KEY_UP)
    assert is_up(ord("k"))
    assert is_down(curses.KEY_DOWN)
    assert is_down(ord("j"))
    assert is_mouse(getattr(curses, "KEY_MOUSE", -1))
    assert is_primary_click(0) is False
