"""Validation and lightweight runtime support for FlossWare TUI Schema 1.0."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

from jsonschema import Draft202012Validator

SCHEMA_VERSION = "flossware.tui/1.0"
SCHEMA_URL = "https://raw.githubusercontent.com/FlossWare/tui-schema/main/schema/tui-1.0.schema.json"


class SchemaError(ValueError):
    """Raised when a TUI schema document is invalid."""


def _load_json(source: str | Path | dict) -> dict:
    if isinstance(source, dict):
        return source
    text = str(source)
    if text.startswith(("https://", "http://")):
        with urlopen(text, timeout=10) as response:  # nosec B310 - explicit schema source
            return json.load(response)
    return json.loads(Path(text).read_text(encoding="utf-8"))


def load_schema(source: str | Path | dict = SCHEMA_URL) -> dict:
    """Load the canonical JSON Schema without embedding its definition."""
    document = _load_json(source)
    if not isinstance(document, dict):
        raise SchemaError("TUI schema must be a JSON object")
    return document


def validate(document: dict, schema: dict | None = None) -> dict:
    """Validate a TUI document and enforce cross-document identity rules."""
    if schema is None:
        schema = load_schema()
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "document"
        raise SchemaError(f"{location}: {first.message}")
    if document.get("schema") != SCHEMA_VERSION:
        raise SchemaError(f"unsupported TUI schema: {document.get('schema')!r}")
    _validate_semantics(document)
    return document


def _validate_semantics(document: dict) -> None:
    identifiers: set[str] = set()
    actions: set[str] = set()

    def identifier(value: object, location: str) -> None:
        if not isinstance(value, str):
            return
        if value in identifiers:
            raise SchemaError(f"duplicate id {value!r} at {location}")
        identifiers.add(value)

    def action(value: object) -> None:
        if isinstance(value, str):
            actions.add(value)

    def widget(item: dict, location: str) -> None:
        identifier(item.get("id"), location)
        action(item.get("action"))
        if item.get("type") == "list":
            for index, child in enumerate(item.get("items", [])):
                identifier(child.get("id"), f"{location}.items[{index}]")
        if item.get("type") == "group":
            for index, child in enumerate(item.get("children", [])):
                widget(child, f"{location}.children[{index}]")

    for index, menu in enumerate(document.get("menus", [])):
        location = f"menus[{index}]"
        identifier(menu.get("id"), location)
        for child_index, item in enumerate(menu.get("items", [])):
            item_location = f"{location}.items[{child_index}]"
            identifier(item.get("id"), item_location)
            action(item.get("action"))

    for index, window in enumerate(document.get("windows", [])):
        location = f"windows[{index}]"
        identifier(window.get("id"), location)
        for field in ("menuBar", "initialFocus"):
            value = window.get(field)
            if value is not None and not isinstance(value, str):
                raise SchemaError(f"{location}.{field} must be an identifier")
        action(window.get("defaultAction"))
        action(window.get("cancelAction"))
        for child_index, item in enumerate(window.get("content", [])):
            widget(item, f"{location}.content[{child_index}]")

    references = {"menuBar": set(), "initialFocus": set(), "selected": set()}
    for window in document.get("windows", []):
        for field in references:
            value = window.get(field)
            if value:
                references[field].add(value)
    for window in document.get("windows", []):
        for item in window.get("content", []):
            if item.get("type") == "list" and item.get("selected"):
                references["selected"].add(item["selected"])

    menu_ids = {m.get("id") for m in document.get("menus", [])}
    if any(value not in menu_ids for value in references["menuBar"]):
        missing = sorted(references["menuBar"] - menu_ids)
        raise SchemaError(f"menuBar references unknown menu id(s): {missing}")

    widget_ids = identifiers
    missing_focus = references["initialFocus"] - widget_ids
    if missing_focus:
        raise SchemaError(f"initialFocus references unknown widget id(s): {sorted(missing_focus)}")
    missing_selection = references["selected"] - widget_ids
    if missing_selection:
        raise SchemaError(f"selected references unknown id(s): {sorted(missing_selection)}")


__all__ = ["SCHEMA_URL", "SCHEMA_VERSION", "SchemaError", "load_schema", "validate"]
