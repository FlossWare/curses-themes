# Reusable TUI Windows

`curses-themes` provides lightweight screen-space windows for applications that need more than a single fixed curses layout.

## Geometry

`Rect` represents `x`, `y`, `width`, and `height`. `SizeConstraints` enforces minimum and optional maximum dimensions. Rectangles can be clamped to terminal bounds.

## Window

`Window` owns geometry and interaction state while leaving application content to an optional draw callback. It supports:

- title-bar dragging
- border and corner resizing
- minimum and maximum size constraints
- terminal-bound clamping
- explicit movable/resizable flags

## Window manager

`WindowManager` manages:

- focus
- z-order
- topmost hit testing
- mouse dispatch for drag and resize
- terminal resize/reclamping
- keyboard movement with arrow keys

The manager keeps application actions outside the library. Consumers decide what a window means and what its content does.

## Deliberate limits

This is a primitive interaction layer, not a full desktop/windowing framework. Persistence, application commands, menus, modal workflows, and business state remain consumer responsibilities.
