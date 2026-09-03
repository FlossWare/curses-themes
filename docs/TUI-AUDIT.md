# TUI Audit

Generic curses input and widget interaction belongs in `curses-themes` so other FlossWare applications can reuse it. Current gaps include mouse capability detection, KEY_MOUSE/getmouse handling, primary click semantics, scroll-aware list hit testing, and consistent mouse behavior for Dropdown and Tabs.

The current implementation in `agent-setup` should be extracted rather than duplicated. `agent-setup` retains domain-specific workflows and persistence.
