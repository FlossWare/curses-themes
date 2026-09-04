# Reusable TUI Input

`curses-themes` provides the low-level keyboard and mouse primitives shared by FlossWare curses applications. Application repositories should keep domain workflows and persistence, while using this package for terminal interaction mechanics.

## Mouse capture

Call `enable_mouse()` when a screen wants mouse interaction. It returns `False` when the terminal or curses implementation cannot provide mouse reporting. Applications can then continue in keyboard-only mode.

Mouse capture is opt-in. This avoids unexpectedly disabling terminal text selection in applications that do not need pointer interaction.

## Events

`mouse_event()` normalizes the current curses mouse event to `(x, y, button_state)`, or returns `None` when the event cannot be read.

`is_mouse(key)` identifies `curses.KEY_MOUSE` without assuming a particular curses implementation.

`is_primary_click(button_state)` treats both primary-button press and click as activation events. `primary_click()` is a convenience helper that reads and filters the current event.

## Lists

`list_index_at()` converts a screen coordinate into an absolute list index and supports scrolling through `scroll_offset` and a visible-row limit.

`resolve_list_mouse()` builds on that hit testing and returns:

- `("activate", index)` for a primary press/click
- `("focus", index)` for other mouse events over a row
- `None` outside the list

This keeps coordinate arithmetic out of application-specific screens.

## Keyboard compatibility

`is_confirm()`, `is_cancel()`, `is_up()`, and `is_down()` normalize the existing Enter, Escape, and vim-style navigation bindings. They are deliberately small so applications can compose them with their own key maps.

## Widgets

`Tabs.handle_mouse()` supports click-to-select using the same primary-click semantics. `Dropdown.choose()` accepts a primary click on its rendered row while retaining its existing keyboard controls.

The API intentionally does not provide a full event-dispatch framework. That belongs in a higher-level TUI application if one is ever needed.
