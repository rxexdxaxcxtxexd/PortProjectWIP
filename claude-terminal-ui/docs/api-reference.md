# API Reference

Complete API documentation for `claude-terminal-ui`.

## Installation

```bash
pip install claude-terminal-ui
```

## Quick Import

```python
import claude_terminal_ui as ui
```

---

## Status Messages

### `print_success(message, *, indent=0, prefix="")`
Print a success message with green color and checkmark symbol.

**Parameters:**
- `message` (str): The message to display
- `indent` (int, optional): Number of spaces to indent. Default: 0
- `prefix` (str, optional): Custom prefix string. Default: ""

**Output:** `✓ message` or `[OK] message` (ASCII fallback)

**Example:**
```python
ui.print_success("File saved successfully")
# Output: ✓ File saved successfully
```

### `print_error(message, *, indent=0, prefix="")`
Print an error message with red color and X symbol.

**Output:** `✗ message` or `[X] message`

### `print_warning(message, *, indent=0, prefix="")`
Print a warning message with yellow color and warning symbol.

**Output:** `⚠ message` or `[!] message`

### `print_info(message, *, indent=0, prefix="")`
Print an info message with cyan color and info symbol.

**Output:** `ℹ message` or `[i] message`

### `print_debug(message, *, indent=0, prefix="")`
Print a debug message with gray color and debug symbol.

**Output:** `⚙ message` or `[D] message`

### Non-Printing Variants

All status functions have non-printing variants that return strings:
- `success(message, **kwargs) -> str`
- `error(message, **kwargs) -> str`
- `warning(message, **kwargs) -> str`
- `info(message, **kwargs) -> str`
- `debug(message, **kwargs) -> str`

---

## Headers and Dividers

### `header(title, *, width=70, char="=", centered=True, color=None)`
Create a major section header.

**Parameters:**
- `title` (str): Header text
- `width` (int, optional): Total width in characters. Default: 70
- `char` (str, optional): Border character. Default: "="
- `centered` (bool, optional): Center the title. Default: True
- `color` (Color, optional): Color for the header. Default: None

**Returns:** str - Formatted header

**Example:**
```python
print(ui.header("MAIN SECTION"))
# ======================================================================
#                            MAIN SECTION
# ======================================================================
```

### `subheader(title, *, width=70, char="-", prefix="")`
Create a subsection header.

**Example:**
```python
print(ui.subheader("Subsection"))
# ----------------------------------------------------------------------
# Subsection
# ----------------------------------------------------------------------
```

### `divider(*, width=70, char="-", label="", prefix="")`
Create a dividing line, optionally with a label.

**Example:**
```python
print(ui.divider())
# ----------------------------------------------------------------------

print(ui.divider(label="Step 1"))
# --- Step 1 -----------------------------------------------------------
```

### `step_header(step, total, description, *, width=70)`
Create a step indicator header.

**Example:**
```python
print(ui.step_header(1, 3, "Processing files..."))
# [1/3] Processing files...
```

---

## Progress Indicators

### `progress_bar(current, total, *, width=50, ...)`
Create a text-based progress bar.

**Parameters:**
- `current` (int): Current progress value
- `total` (int): Total/maximum value
- `width` (int, optional): Bar width in characters. Default: 50
- `filled_char` (str, optional): Character for filled portion
- `empty_char` (str, optional): Character for empty portion
- `show_percentage` (bool, optional): Show percentage. Default: True
- `prefix` (str, optional): Text before bar
- `suffix` (str, optional): Text after bar

**Returns:** str - Formatted progress bar

**Example:**
```python
print(ui.progress_bar(75, 100, width=40))
# [██████████████████████████████          ] 75%
```

### `step_indicator(current, total, message="")`
Format a step indicator.

**Example:**
```python
print(ui.step_indicator(2, 5, "Processing files"))
# [2/5] Processing files
```

### `Spinner` Class
Animated spinner for long-running operations.

**Usage:**
```python
# Context manager (recommended)
with ui.spinner("Loading data"):
    long_operation()

# Manual control
spinner = ui.Spinner("Processing")
spinner.start()
do_work()
spinner.stop("Complete!")
```

**Parameters:**
- `message` (str): Message to display. Default: "Working"
- `frames` (list, optional): Custom spinner frames
- `interval` (float, optional): Animation interval in seconds. Default: 0.1

### `spinner()` Context Manager
Convenience context manager for spinners.

**Example:**
```python
with ui.spinner("Loading"):
    time.sleep(2)
```

---

## Tables (Advanced Components)

### `key_value(items, *, separator=":", key_width=None, indent=0, key_color=None)`
Format key-value pairs.

**Parameters:**
- `items` (Dict[str, Any]): Key-value pairs to display
- `separator` (str, optional): Separator between key and value. Default: ":"
- `key_width` (int, optional): Fixed width for keys. Default: auto-calculated
- `indent` (int, optional): Left indentation. Default: 0
- `key_color` (Color, optional): Color for keys

**Example:**
```python
ui.key_value({
    "Project": "claude-terminal-ui",
    "Version": "0.1.0",
    "Status": "Active"
})
#   Project:  claude-terminal-ui
#   Version:  0.1.0
#    Status:  Active
```

### `table(data, headers=None, *, column_widths=None, ...)`
Create a formatted table.

**Parameters:**
- `data` (List[List[str]]): Rows of data
- `headers` (List[str], optional): Column headers
- `column_widths` (List[int], optional): Explicit column widths
- `align` (str, optional): Text alignment ("left", "right", "center"). Default: "left"
- `border` (bool, optional): Draw borders. Default: True
- `header_style` (Color, optional): Color for header row

**Example:**
```python
ui.table(
    data=[
        ["Alice", "Engineer", "100"],
        ["Bob", "Designer", "85"]
    ],
    headers=["Name", "Role", "Score"]
)
```

---

## Design Tokens

### Colors
```python
from claude_terminal_ui.tokens import Colors

Colors.SUCCESS   # Green
Colors.ERROR     # Red
Colors.WARNING   # Yellow
Colors.INFO      # Cyan
Colors.DEBUG     # Gray
Colors.PRIMARY   # White
Colors.SECONDARY # Light gray
Colors.MUTED     # Dark gray
```

### Symbols
```python
from claude_terminal_ui.tokens import Symbols

Symbols.SUCCESS   # ✓ or [OK]
Symbols.ERROR     # ✗ or [X]
Symbols.WARNING   # ⚠ or [!]
Symbols.INFO      # ℹ or [i]
Symbols.BULLET    # • or *
Symbols.ARROW_RIGHT # → or ->
```

### Spacing Constants
```python
from claude_terminal_ui.tokens import DEFAULT_WIDTH, WIDE_WIDTH

DEFAULT_WIDTH  # 70 characters
WIDE_WIDTH     # 100 characters
```

---

## Terminal Capabilities

### `get_capabilities()`
Get detected terminal capabilities.

**Returns:** `TerminalCapabilities` with fields:
- `color_support`: ColorSupport enum (NONE/BASIC/EXTENDED/TRUECOLOR)
- `unicode_support`: bool
- `width`: int (terminal columns)
- `height`: int (terminal lines)
- `is_interactive`: bool
- `is_windows`: bool
- `terminal_name`: str
- `supports_hyperlinks`: bool

**Example:**
```python
from claude_terminal_ui.core import get_capabilities

caps = get_capabilities()
if caps.unicode_support:
    print("Unicode symbols available!")
```

### `reset_capabilities()`
Reset cached capabilities (useful for testing).

---

## Environment Variables

The library respects standard environment variables:

- `NO_COLOR` - Disable all colors
- `FORCE_COLOR` - Force color output
- `TERM` - Terminal type detection
- `COLORTERM` - Truecolor detection
- `WT_SESSION` - Windows Terminal detection

**Example:**
```bash
# Disable colors
NO_COLOR=1 python script.py

# Force truecolor
FORCE_COLOR=3 python script.py
```

---

## Type Hints

All functions include type hints for better IDE support:

```python
def header(
    title: str,
    *,
    width: int = 70,
    char: str = "=",
    centered: bool = True,
    color: Optional[Color] = None
) -> str:
    ...
```

---

## Exception Handling

The library is designed to never crash due to terminal issues:

- Missing terminal → Safe defaults (80x24, no color, ASCII)
- Encoding errors → Automatic ASCII fallback
- Redirected output → Detects and adapts

No try/except needed in your code!