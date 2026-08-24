from curses_themes import Dropdown, Option, Table, Tabs


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


def test_table_accepts_rows():
    table = Table(["A", "B"], [(1, "two")])
    assert table.headers == ["A", "B"]
    assert table.rows == [["1", "two"]]
