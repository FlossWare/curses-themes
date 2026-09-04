import curses
from unittest.mock import patch

from curses_tui import Dropdown, Option, Table, Tabs


def test_dropdown_options():
    dropdown = Dropdown([Option("a", "Alpha"), "Beta"], selected=1)
    assert dropdown.options[0].value == "a"
    assert dropdown.options[1].label == "Beta"
    assert dropdown.selected == 1


def test_tabs_handle():
    tabs = Tabs(["One", "Two", "Three"])
    assert tabs.handle(ord("3"))
    assert tabs.selected == 2
    assert tabs.handle(ord("h"))
    assert tabs.selected == 1


def test_tabs_handle_mouse_selects_clicked_tab():
    clicked = getattr(curses, "BUTTON1_CLICKED", 0)
    if not clicked:
        return
    tabs = Tabs(["One", "Two", "Three"])
    assert tabs.handle_mouse((8, 2, clicked), y=2)
    assert tabs.selected == 1
    assert not tabs.handle_mouse((40, 2, clicked), y=2)


def test_dropdown_choose_accepts_mouse_click_on_row():
    clicked = getattr(curses, "BUTTON1_CLICKED", 0)
    key_mouse = getattr(curses, "KEY_MOUSE", -1)
    if not clicked or key_mouse < 0:
        return

    class Window:
        def __init__(self):
            self.keys = [key_mouse]

        def addnstr(self, *args):
            return None

        def getch(self):
            return self.keys.pop(0)

    dropdown = Dropdown(["Alpha"])
    with patch("curses_tui.widgets.mouse_event", return_value=(4, 3, clicked)):
        assert dropdown.choose(Window(), 3, 0, 20) == "Alpha"


def test_table_accepts_rows():
    table = Table(["A", "B"], [(1, "two")])
    assert table.headers == ["A", "B"]
    assert table.rows == [["1", "two"]]
