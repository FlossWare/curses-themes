# TUI Architecture

`curses-themes` is the reusable curses/TUI foundation for FlossWare applications. Applications should own domain workflows and state, while reusable terminal interaction primitives belong here.

## Reusable responsibilities

- Theme and color management
- Reusable widgets
- Keyboard input normalization
- Mouse capability detection and fallback
- Mouse event decoding
- Primary-button press/click semantics
- Screen-coordinate to widget/list hit testing
- Scroll-aware list navigation
- Focus and selection behavior
- Popup/list interaction primitives
- Testable input/interaction helpers

## Application responsibilities

Applications such as `agent-setup` should own:

- Domain-specific screens and workflows
- Profile/provider/agent state
- Persistence of application state
- Domain-specific actions triggered by widget events

Applications should consume `curses-themes` primitives instead of implementing their own low-level curses mouse and list interaction logic.

## Current gap

The current `curses-themes` package exposes reusable widgets such as `Dropdown`, `Tabs`, and `Table`, but its public API does not yet expose the mouse/input helpers now implemented in `agent-setup`. The `agent-setup` implementation should therefore be treated as the reference behavior for extraction, not as the permanent home of the shared implementation.

## Extraction contract

The reusable input layer should support:

1. Keyboard-only operation when mouse reporting is unavailable.
2. `KEY_MOUSE` event detection and safe `getmouse()` handling.
3. Primary-button press and click activation.
4. Coordinate hit testing with explicit widget/list origin.
5. Scroll-aware hit testing with visible-row bounds.
6. Distinguishing activation from focus/hover.
7. No activation for clicks outside the interactive region.
8. Unit tests independent of a live terminal, plus application-level integration tests.
9. A stable public API so consuming applications do not import private implementation modules.

`agent-setup` should retain only the thin integration layer that maps domain actions such as selecting a profile onto these primitives.
