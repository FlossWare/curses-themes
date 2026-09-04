"""Tests for the canonical FlossWare TUI Schema 1.0 adapter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from curses_tui import SchemaError, build_menus, build_window_manager, validate

FIXTURE = Path(__file__).parent / "fixtures" / "tui-1.0.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_valid_1_0_document_validates() -> None:
    document = load_fixture()
    assert validate(document)["schema"] == "flossware.tui/1.0"


def test_duplicate_ids_are_rejected() -> None:
    document = load_fixture()
    document["windows"][0]["content"][1]["id"] = "heading"
    with pytest.raises(SchemaError, match="duplicate id"):
        validate(document)


def test_unknown_menu_reference_is_rejected() -> None:
    document = load_fixture()
    document["windows"][0]["menuBar"] = "missing"
    with pytest.raises(SchemaError, match="unknown menu"):
        validate(document)


def test_unknown_focus_reference_is_rejected() -> None:
    document = load_fixture()
    document["windows"][0]["initialFocus"] = "missing"
    with pytest.raises(SchemaError, match="initialFocus"):
        validate(document)


def test_actions_remain_identifiers() -> None:
    document = load_fixture()
    menu = build_menus(document)["file"]
    assert menu.activate(0) == "project.open"
    assert menu.activate(1) == "app.exit"


def test_declarative_windows_map_to_reusable_manager() -> None:
    document = load_fixture()
    manager = build_window_manager(document, 100, 40)
    assert len(manager.windows) == 1
    window = manager.windows[0]
    assert window.title == "Setup"
    assert window.rect.width == 60
    assert window.rect.height == 12
    assert window.constraints.min_width == 20
    assert window.constraints.min_height == 6
