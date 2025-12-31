# Claude Terminal UI - Examples

This directory contains example applications and demos showcasing the Claude Terminal UI Design System.

## Interactive Showcase Demo

The **demo_showcase.py** is a comprehensive, portfolio-ready interactive demonstration of all components in the design system.

### Features

- **Interactive Menu System**: Explore components by category
- **Before/After Comparisons**: See raw print vs UI components side-by-side
- **Real-World Examples**: Complete application scenarios
- **All Component Variants**: Status messages, headers, progress indicators, tables, trees, and panels
- **Terminal Capability Demo**: Shows auto-detection and graceful degradation

### Running the Demo

```bash
# From the repository root
python examples/demo_showcase.py

# Or from the examples directory
cd examples
python demo_showcase.py
```

### Component Categories

1. **Status Messages** - Success, error, warning, info, debug indicators
2. **Headers & Dividers** - Section headers, subsections, and dividers
3. **Progress Indicators** - Progress bars, spinners, step indicators
4. **Tables** - Key-value pairs, data tables, statistics panels
5. **Trees & Lists** - Hierarchical tree structures and nested lists
6. **Panels & Boxes** - Bordered content panels and info boxes
7. **Real-World Examples** - Complete application scenarios (deployment, data processing)
8. **Before/After Comparison** - Visual comparison of raw vs styled output
9. **Terminal Capabilities** - Auto-detection and fallback behavior

### Navigation

- **0-9**: Select a demo category
- **0**: Run all demos sequentially
- **q**: Quit the showcase

### Portfolio Use

This demo is designed to be portfolio-ready:
- Professional presentation with clear labeling
- Real-world use case examples
- Demonstrates technical skills in CLI/TUI design
- Shows understanding of cross-platform compatibility
- Exhibits clean code architecture

### Other Examples

- **demo_all.py** - Simple sequential demo of all components
- **session_display.py** - Example of session state display
- **quick_test.py** - Quick component testing
- **test_detection.py** - Terminal capability detection testing

## Usage in Your Projects

To use these components in your own CLI applications:

```python
import claude_terminal_ui as ui

# Status messages
ui.print_success("Operation completed!")
ui.print_error("Connection failed")

# Progress tracking
for i in range(100):
    print(f"\r{ui.progress_bar(i, 100)}", end="", flush=True)

# Data display
data = {"Name": "John", "Status": "Active"}
ui.print_key_value(data)

# Structured output
ui.print_header("Application Results")
ui.print_table(data_rows, headers=["ID", "Status", "Count"])
```

See the demo code for more examples and advanced usage patterns.
