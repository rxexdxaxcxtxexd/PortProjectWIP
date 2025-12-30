# Claude Terminal UI

**Professional terminal UI design system for Python CLI applications**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`claude-terminal-ui` is a comprehensive design system for creating beautiful, consistent terminal output in Python applications. It features:

- 🎨 **Semantic color system** with automatic terminal capability detection
- 🔤 **Unicode symbols** with ASCII fallbacks for maximum compatibility
- 📊 **Rich components**: status messages, headers, progress bars, tables, and more
- 🎭 **Theme system** for customization
- 🖥️ **Cross-platform** - works on Windows, macOS, and Linux
- ♿ **Accessible** - graceful degradation for all terminal types

## Quick Start

```python
from claude_terminal_ui import ui

# Status messages
ui.print_success("Operation completed")
ui.print_error("Something went wrong")
ui.print_warning("Disk space running low")

# Headers
ui.header("SECTION TITLE")
ui.subheader("Subsection")

# Progress indicators
print(ui.step_indicator(1, 3, "Processing files..."))

# Tables
ui.key_value({
    "Project": "claude-terminal-ui",
    "Version": "0.1.0",
    "Status": "Development"
})
```

## Installation

```bash
pip install claude-terminal-ui
```

For full features (progress bars, advanced tables):
```bash
pip install claude-terminal-ui[full]
```

## Features

### Automatic Terminal Detection

The library automatically detects your terminal's capabilities and adjusts output accordingly:

- **Color support**: None → 16 colors → 256 colors → Truecolor
- **Unicode support**: Falls back to ASCII symbols on older terminals
- **Width detection**: Adapts to terminal size

### Components

- **Status Messages**: `success()`, `error()`, `warning()`, `info()`, `debug()`
- **Headers**: `header()`, `subheader()`, `divider()`
- **Progress**: `progress_bar()`, `spinner()`, `step_indicator()`
- **Tables**: `table()`, `key_value()`, `stats_panel()`
- **Trees**: `tree()`, `nested_list()`
- **Interactive**: `prompt()`, `select()`, `confirm()`

### Design Tokens

Consistent design language with semantic tokens:

- **Colors**: SUCCESS, ERROR, WARNING, INFO, DEBUG
- **Symbols**: ✓ ✗ ⚠ ℹ (with ASCII fallbacks)
- **Spacing**: Standardized widths and padding

## Documentation

- [API Reference](docs/api-reference.md)
- [Design System Guide](docs/design-system.md)
- [Migration Guide](docs/migration.md)
- [Examples](examples/)

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/claude_terminal_ui --cov-report=html

# Format code
black src/ tests/
ruff check src/ tests/

# Type checking
mypy src/
```

## Portfolio Project

This design system was created as part of a portfolio demonstration of:
- **UX thinking** applied to developer tools
- **Design systems** for terminal interfaces
- **Cross-platform compatibility** handling
- **API design** for Python libraries

See the [Terminal UI/UX Analysis](../TERMINAL_UI_UX_ANALYSIS.md) for the design research and decision-making process.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Created by Layden as part of the Context-Aware Memory Management System portfolio project.
