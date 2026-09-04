# curses-tui

**Lightweight terminal UI and theme support for Python curses applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Inspired by [FlossWare curses-java](https://github.com/FlossWare/curses-java), this library provides reusable terminal UI primitives and professional theme support for Python's standard `curses` module.

## Role in FlossWare TUI

`curses-tui` is the Python implementation layer for the language-neutral [`FlossWare/tui-schema`](https://github.com/FlossWare/tui-schema) contract. The schema defines portable JSON structure and semantic actions; this library provides native terminal rendering, interaction, windows, menus, focus, geometry, and themes.

The canonical contract is **JSON only**. YAML and XML are intentionally excluded. Application actions remain semantic identifiers and are resolved by the consuming application.

## Features

- 🎨 Built-in professional and retro themes
- 🪟 Reusable windows, dialogs, popups, and panels
- 📋 Reusable menus, menu items, and accelerators
- 🎯 Focus, keyboard, mouse, geometry, movement, and resizing primitives
- 🔌 Pluggable architecture for application-specific integration
- 🔄 Runtime theme switching
- 🖥️ Terminal-aware color handling with fallbacks
- 📦 Python standard-library curses foundation
- 🧪 Thoroughly tested
- 📚 Designed to consume the `tui-schema` 1.0 contract without duplicating it

## Python package

The Python distribution is `curses-tui` and the import namespace is `curses_tui`.

```python
from curses_tui import ThemeManager, WindowManager
```

The former `curses_themes` package name is intentionally unsupported. This is a breaking package rename.

## TUI schema integration

The shared contract is maintained in [`FlossWare/tui-schema`](https://github.com/FlossWare/tui-schema). Version 1.0 defines typed widgets, top-level menus, semantic actions, focus, window behavior, absolute terminal-cell layout, and named themes.

`curses-tui` MUST NOT redefine the schema. It interprets supported schema documents and maps their portable concepts onto native Python/curses primitives.

## Related Projects

- [tui-schema](https://github.com/FlossWare/tui-schema) - Canonical language-neutral JSON TUI contract
- [curses-java](https://github.com/FlossWare/curses-java) - Java terminal UI library
- [agent-setup](https://github.com/FlossWare/agent-setup) - FlossWare setup application consuming the shared TUI implementation

## License

MIT - See [LICENSE](LICENSE) for details.

## Author

**FlossWare** - [https://github.com/FlossWare](https://github.com/FlossWare)
