# TUI Input Extraction Plan

## Source implementation

`FlossWare/agent-setup` currently contains a curses input helper module implementing mouse capability detection, `getmouse()` decoding, primary-button detection, coordinate hit testing, and scroll-aware list event resolution.

## Move to curses-themes

The following are library-level behavior:

- `enable_mouse()`
- safe mouse event decoding
- `is_mouse()`
- primary button masks and activation detection
- list hit testing
- scroll-aware list hit testing
- activation versus focus event semantics
- keyboard input predicates where they are generic rather than setup-specific

These should be exposed through a public, documented API.

## Keep in agent-setup

The following remain application behavior:

- profile persistence
- profile names and profile ordering
- setup workflow transitions
- provider/model configuration actions
- domain-specific popup contents

## Widgets

`curses-themes` already has `Dropdown`, `Tabs`, and `Table`. The audit found that `Dropdown` is described as keyboard/mouse-friendly but currently handles only keyboard input in its `choose()` loop. `Tabs` is described as mouse-supported but its current `handle()` method handles keyboard input only and has no mouse coordinate/event API. These are candidates for completing the widget contract as part of the extraction.

## Compatibility

The first extraction should preserve existing keyboard behavior and make mouse support additive. `agent-setup` should depend on a released/pinned `curses-themes` version containing the extracted API, then remove duplicate low-level mouse helpers.

## Testing

`curses-themes` should gain deterministic tests for:

- mouse capability fallback
- `KEY_MOUSE` recognition
- `getmouse()` error handling
- primary press/click activation
- list hit testing
- scroll and visible bounds
- outside-list behavior
- widget mouse activation
- keyboard regression behavior

`agent-setup` should retain integration tests proving that profile selection invokes its own persistence/action layer when the reusable widget reports activation.
