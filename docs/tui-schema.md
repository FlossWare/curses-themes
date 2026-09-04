# TUI Schema 1.0

`curses-tui` consumes the canonical language-neutral JSON contract defined by [`FlossWare/tui-schema`](https://github.com/FlossWare/tui-schema).

The implementation does **not** copy or redefine the canonical JSON Schema. By default, `curses_tui.schema` loads the published 1.0 schema from the canonical repository; callers may also supply a local schema document or already-loaded schema object for controlled/offline deployments.

## Validation

```python
from curses_tui import validate

validate(document)
```

Validation has two layers:

1. JSON Schema Draft 2020-12 validation against `flossware.tui/1.0`.
2. Semantic validation for document-wide identifier uniqueness and references such as `menuBar`, `initialFocus`, and list `selected` values.

Invalid documents raise `SchemaError` with a deterministic location and message.

## Runtime adapter

```python
from curses_tui import build_menus, build_window_manager

menus = build_menus(document)
manager = build_window_manager(document, screen_width, screen_height)
```

The adapter maps schema menus to the reusable `Menu`/`MenuItem` primitives and windows to `Window`/`WindowManager`. Declarative widgets are rendered from their typed `type` values, including labels, text inputs, checkboxes, lists, buttons, separators, and recursive groups.

Schema actions remain **identifiers** such as `project.save` or `app.exit`. They are never evaluated as Python code. Application code owns the action handler:

```python
result = dispatch_action("project.save", application_action_handler)
```

This keeps `curses-tui` responsible for reusable terminal interaction while the consuming application owns domain behavior, state, persistence, and workflows.

## Contract boundary

`tui-schema` defines what a terminal UI declares. `curses-tui` defines how that declaration is rendered and interacted with. Applications such as `agent-setup` define what each semantic action actually does.

JSON is the canonical interchange format. YAML and XML are intentionally not part of this contract.
