# Table Formatting Components

Comprehensive table formatting for terminal UI applications.

## Features

- **Key-Value Pairs**: Aligned key-value displays
- **Data Tables**: Full tables with headers, borders, and alignment
- **Statistics Panels**: Grid and list layouts for summary stats
- **Unicode Support**: Automatic fallback to ASCII for compatibility
- **Color Support**: Optional header and value coloring
- **Width Control**: Standard (70) and wide (100) width options

## Functions

### `key_value(items, **options)`

Format dictionary items as aligned key-value pairs.

**Example:**
```python
import claude_terminal_ui as ui

session = {
    "Session ID": "5150ba34",
    "Started": "2025-12-29 12:49",
    "Tokens": "1,234 / 200,000",
}

print(ui.key_value(session, indent=2))
```

**Output:**
```
  Session ID: 5150ba34
  Started   : 2025-12-29 12:49
  Tokens    : 1,234 / 200,000
```

**Options:**
- `width` (int): Maximum width (default: 70)
- `indent` (int): Left indentation in spaces
- `align_colon` (bool): Align colons at same column (default: True)
- `value_color` (Color): Optional color for values
- `key_width` (int): Fixed key column width (auto if None)

### `table(data, headers, **options)`

Format a full data table with borders and alignment.

**Example:**
```python
headers = ["Key", "Status", "Count"]
data = [
    ["BOPS-123", "Done", "5"],
    ["BOPS-124", "Active", "12"],
]

print(ui.table(data, headers))
```

**Output:**
```
+----------+--------+-------+
| Key      | Status | Count |
+----------+--------+-------+
| BOPS-123 | Done   | 5     |
| BOPS-124 | Active | 12    |
+----------+--------+-------+
```

**Options:**
- `width` (int): Maximum width (default: 70)
- `align` (List[str]): Column alignment - 'left', 'right', 'center'
- `header_color` (Color): Color for header row
- `show_borders` (bool): Show table borders (default: True)
- `compact` (bool): Minimal spacing (default: False)

**Column Alignment:**
```python
# Right-align numeric columns
headers = ["Name", "Amount", "Status"]
data = [["Invoice #1", "1,234.56", "Paid"]]

print(ui.table(
    data,
    headers,
    align=["left", "right", "center"]
))
```

### `stats_panel(stats, **options)`

Format statistics in grid or list layout.

**Example (Grid):**
```python
stats = {
    "Total": 100,
    "Active": 25,
    "Complete": 70,
    "Pending": 5,
}

print(ui.stats_panel(
    stats,
    title="PROJECT STATS",
    layout="grid",
    columns=2
))
```

**Output:**
```
┌────────────────────────────────────┐
│         PROJECT STATS              │
├────────────────────────────────────┤
│ Total: 100         Active: 25      │
│ Complete: 70       Pending: 5      │
└────────────────────────────────────┘
```

**Example (List):**
```python
print(ui.stats_panel(
    stats,
    title="PROJECT STATS",
    layout="list"
))
```

**Output:**
```
────────────────────────────────────
PROJECT STATS
────────────────────────────────────
  Total   : 100
  Active  : 25
  Complete: 70
  Pending : 5
```

**Options:**
- `title` (str): Optional panel title
- `width` (int): Panel width (default: 70)
- `layout` (str): "grid" (multi-column) or "list" (single column)
- `columns` (int): Number of columns for grid layout (default: 2)
- `show_borders` (bool): Show panel borders (default: True)
- `title_color` (Color): Optional color for title

## Print Variants

Convenience functions that print directly:

```python
# Instead of: print(ui.key_value(...))
ui.print_key_value(...)

# Instead of: print(ui.table(...))
ui.print_table(...)

# Instead of: print(ui.stats_panel(...))
ui.print_stats_panel(...)
```

## Width Constants

Use predefined width constants for consistency:

```python
from claude_terminal_ui.tokens.spacing import DEFAULT_WIDTH, WIDE_WIDTH

# Standard width (70 chars) - most outputs
print(ui.table(data, headers, width=DEFAULT_WIDTH))

# Wide width (100 chars) - audit reports, wide tables
print(ui.table(data, headers, width=WIDE_WIDTH))
```

## Real-World Examples

### Session Information Display

```python
import claude_terminal_ui as ui

print(ui.header("SESSION INFORMATION"))

session_info = {
    "Session ID": "5150ba34",
    "Started": "2025-12-29 12:49:35",
    "Duration": "1h 42m",
    "Messages": 42,
}

ui.print_key_value(
    session_info,
    indent=2,
    value_color=ui.tokens.colors.Colors.INFO
)
```

### Context Monitor Output

```python
print(ui.header("CONTEXT WINDOW STATUS"))

context = {
    "Estimated Tokens": "~45,000 / 200,000",
    "Usage": "~22.5%",
    "Remaining": "~155,000 tokens",
}

ui.print_key_value(context, indent=2)

# Progress bar
print()
bar_width = 50
filled = int(0.225 * bar_width)
bar = '=' * filled + '-' * (bar_width - filled)
print(f"  [{bar}]")
```

### Jira Audit Report

```python
from claude_terminal_ui.tokens.spacing import WIDE_WIDTH

print(ui.header("BOPS AUDIT REPORT", width=WIDE_WIDTH))

# Summary stats
summary = {
    "Total Tickets": 50,
    "With Account": "35 (70%)",
    "Without Account": "15 (30%)",
}

print(ui.subheader("Summary"))
ui.print_key_value(summary, indent=2)

# Tickets table
print()
print(ui.subheader("Recent Tickets"))

headers = ["Key", "Status", "Account", "Summary"]
tickets = [
    ["BOPS-3665", "IN CSG QA/UVT", "BargeOps Maintenance", "Crews - Boat Detail..."],
    ["BOPS-3663", "IN CSG QA/UVT", "BargeOps Maintenance", "Onboard: Night mode..."],
]

ui.print_table(tickets, headers, width=WIDE_WIDTH)
```

### Performance Comparison

```python
print(ui.header("PERFORMANCE METRICS"))

headers = ["Metric", "Before", "After", "Change"]
data = [
    ["Load Time", "2.5s", "0.8s", "-68%"],
    ["Memory Usage", "450MB", "280MB", "-38%"],
    ["API Calls", "125", "45", "-64%"],
]

ui.print_table(
    data,
    headers,
    align=["left", "right", "right", "right"]
)
```

### Sprint Statistics

```python
stats = {
    "Total Stories": 24,
    "Completed": 20,
    "In Progress": 3,
    "Blocked": 1,
    "Velocity": "45 pts",
    "Completion": "83%",
}

ui.print_stats_panel(
    stats,
    title="SPRINT 12 SUMMARY",
    layout="grid",
    columns=2,
    title_color=ui.tokens.colors.Colors.SUCCESS
)
```

## Design Notes

### Unicode Detection

Tables automatically use box-drawing characters (┌─┐│└┘) when Unicode is supported, falling back to ASCII (+|-) otherwise. Detection is based on `sys.stdout.encoding`.

### Color Support

Header and value colors are automatically disabled on terminals without color support. Uses the global capability detection system.

### Width Behavior

- `width` parameter is a maximum guideline
- Tables may exceed width if content requires it
- No automatic text wrapping (truncate content before passing to table functions)

### Alignment

Valid alignment values:
- `"left"` - Left-aligned (default)
- `"right"` - Right-aligned (numbers, amounts)
- `"center"` - Center-aligned

### Cell Padding

- Default: `CELL_PADDING = 1` (1 space on each side)
- Compact mode: No padding (`compact=True`)

## Integration

Import the table components:

```python
# Full import
import claude_terminal_ui as ui
ui.print_table(...)

# Direct import
from claude_terminal_ui import table, key_value, stats_panel

# Component-level import
from claude_terminal_ui.components.tables import table
```

## Testing

Run the comprehensive test suite:

```bash
python test_tables.py
```

Run the interactive demo:

```bash
python demo_tables.py
```

## Related Components

- `headers.py` - Section headers and dividers
- `status.py` - Status messages (success, error, warning)
- `progress.py` - Progress bars and spinners
- `spacing.py` - Width and spacing constants
- `colors.py` - Color definitions and support
