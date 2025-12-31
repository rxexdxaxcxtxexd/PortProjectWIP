# Trees and Panels Components

Hierarchical display and boxed content components for terminal output.

## Overview

Two new component modules have been added to `claude-terminal-ui`:

1. **trees.py** - Hierarchical tree structures and nested lists
2. **panels.py** - Boxed content with borders and titles

Both components follow the existing design patterns:
- Automatic Unicode/ASCII fallback based on terminal capabilities
- Color support with graceful degradation
- Consistent API with other components
- Type hints and comprehensive documentation

## Trees Component

### Functions

#### `tree(root, *, indent=0, prefix="", color=None)`

Create a tree structure with branch characters.

**Parameters:**
- `root`: TreeNode or string label for the root
- `indent`: Initial indentation level (spaces)
- `prefix`: Prefix string for each line
- `color`: Default color for nodes without explicit colors

**Example:**
```python
from claude_terminal_ui.components.trees import tree, TreeNode
from claude_terminal_ui.tokens.colors import Colors

# Create a tree structure
root = TreeNode("Files", [
    TreeNode("src/", color=Colors.INFO),
    TreeNode("tests/", color=Colors.SUCCESS),
])

print(tree(root))
```

**Output (ASCII mode):**
```
Files
|-- src/
`-- tests/
```

**Output (Unicode mode):**
```
Files
├── src/
└── tests/
```

#### `nested_list(items, *, indent=0, bullet="•", prefix="", color=None, level_indent=2)`

Create an indented nested list.

**Parameters:**
- `items`: List of items (strings or tuples for nesting)
- `indent`: Initial indentation level
- `bullet`: Bullet character (default: "•")
- `prefix`: Prefix string for each line
- `color`: Color for items
- `level_indent`: Spaces per nesting level

**Example:**
```python
from claude_terminal_ui.components.trees import nested_list

items = [
    "First item",
    ("Nested", ["Child 1", "Child 2"]),
    "Last item"
]

print(nested_list(items))
```

**Output:**
```
* First item
* Nested
  * Child 1
  * Child 2
* Last item
```

#### `simple_tree(items, *, title=None, indent=0, prefix="", color=None)`

Create a simple tree from a flat list of items.

**Parameters:**
- `items`: List of item labels
- `title`: Optional title for the tree
- `indent`: Initial indentation level
- `prefix`: Prefix string
- `color`: Color for items

**Example:**
```python
from claude_terminal_ui.components.trees import simple_tree

print(simple_tree(["Item 1", "Item 2", "Item 3"], title="Tasks"))
```

**Output:**
```
Tasks
|-- Item 1
|-- Item 2
`-- Item 3
```

### TreeNode Class

Represents a node in a tree structure.

**Constructor:**
```python
TreeNode(label: str, children: List[TreeNode] = None, color: Color = None)
```

**Example:**
```python
from claude_terminal_ui.components.trees import TreeNode
from claude_terminal_ui.tokens.colors import Colors

root = TreeNode(
    "Project",
    children=[
        TreeNode("src/", color=Colors.INFO),
        TreeNode("tests/", children=[
            TreeNode("test_a.py"),
            TreeNode("test_b.py")
        ])
    ]
)
```

## Panels Component

### Functions

#### `panel(content, *, title=None, width=None, color=None, title_color=None, padding=1, align="left")`

Create a panel with bordered content.

**Parameters:**
- `content`: Text content to display
- `title`: Optional title displayed at the top
- `width`: Panel width (auto-sized if None)
- `color`: Border color
- `title_color`: Title color (defaults to color)
- `padding`: Internal padding (spaces)
- `align`: Content alignment ("left", "center", "right")

**Example:**
```python
from claude_terminal_ui.components.panels import panel
from claude_terminal_ui.tokens.colors import Colors

print(panel("Hello World", title="Greeting", color=Colors.INFO))
```

**Output (ASCII mode):**
```
+- Greeting -------+
| Hello World      |
+------------------+
```

**Output (Unicode mode):**
```
┌─ Greeting ───────┐
│ Hello World      │
└──────────────────┘
```

#### `box(content, *, width=None, color=None, padding=1)`

Create a simple box around content (no title).

**Example:**
```python
from claude_terminal_ui.components.panels import box

print(box("Important"))
```

**Output:**
```
+-----------+
| Important |
+-----------+
```

#### `info_panel(message, *, title=None, width=None, panel_type="info")`

Create an informational panel with appropriate icon and color.

**Panel Types:**
- `"info"` - Cyan with info icon
- `"success"` - Green with checkmark
- `"warning"` - Yellow with warning icon
- `"error"` - Red with error icon
- `"debug"` - Gray with debug icon

**Example:**
```python
from claude_terminal_ui.components.panels import info_panel

print(info_panel("Task completed", panel_type="success"))
```

**Output:**
```
+------------------+
| ✓ Task completed |
+------------------+
```

#### `titled_box(items, *, title, width=None, color=None, bullet="•")`

Create a box with a title and list of items.

**Example:**
```python
from claude_terminal_ui.components.panels import titled_box
from claude_terminal_ui.tokens.colors import Colors

tasks = ["Run tests", "Build project", "Deploy"]
print(titled_box(tasks, title="Next Steps", color=Colors.WARNING))
```

**Output:**
```
+- Next Steps --------+
| * Run tests         |
| * Build project     |
| * Deploy            |
+---------------------+
```

#### `compact_panel(key_values, *, title=None, width=None, color=None)`

Create a compact panel displaying key-value pairs.

**Example:**
```python
from claude_terminal_ui.components.panels import compact_panel

data = {
    "ID": "5150ba34",
    "Status": "Active",
    "Duration": "2h 15m"
}
print(compact_panel(data, title="Session"))
```

**Output:**
```
+- Session ------------+
| ID      : 5150ba34   |
| Status  : Active     |
| Duration: 2h 15m     |
+----------------------+
```

## Cross-Platform Compatibility

Both components automatically detect terminal capabilities and fall back to ASCII mode when Unicode is not supported:

### Tree Characters
- **Unicode**: `├──`, `└──`, `│`
- **ASCII**: `|--`, `` `-- ``, `|`

### Box Characters
- **Unicode**: `┌`, `─`, `┐`, `│`, `└`, `┘`
- **ASCII**: `+`, `-`, `+`, `|`, `+`, `+`

### Bullet Points
- **Unicode**: `•`
- **ASCII**: `*`

## Usage Examples

### Session Checkpoint Display

```python
from claude_terminal_ui.components.trees import tree, TreeNode
from claude_terminal_ui.components.panels import compact_panel, titled_box
from claude_terminal_ui.tokens.colors import Colors

# Session metadata
session_data = {
    "Session ID": "5150ba34",
    "Started": "2025-12-30 12:49:35",
    "Duration": "2h 15m",
}
print(compact_panel(session_data, title="Session Info", color=Colors.INFO))
print()

# Resume points as tree
resume_root = TreeNode("Tasks", [
    TreeNode("In Progress", [
        TreeNode("Fix bug #123")
    ]),
    TreeNode("Next", [
        TreeNode("Run tests"),
        TreeNode("Deploy")
    ])
])
print(tree(resume_root))
print()

# Next steps
steps = ["Review code", "Update docs", "Create PR"]
print(titled_box(steps, title="Next Steps", color=Colors.WARNING))
```

### File Tree Display

```python
from claude_terminal_ui.components.trees import tree, TreeNode
from claude_terminal_ui.tokens.colors import Colors

project = TreeNode("my-project/", [
    TreeNode("src/", [
        TreeNode("main.py", color=Colors.INFO),
        TreeNode("utils.py", color=Colors.INFO)
    ]),
    TreeNode("tests/", [
        TreeNode("test_main.py", color=Colors.SUCCESS)
    ])
])

print(tree(project))
```

### Progress Dashboard

```python
from claude_terminal_ui.components.panels import titled_box, compact_panel
from claude_terminal_ui.tokens.colors import Colors

# Completed tasks
completed = ["Task 1", "Task 2", "Task 3"]
print(titled_box(completed, title="Completed", color=Colors.SUCCESS))
print()

# Statistics
stats = {
    "Total": "10",
    "Completed": "3 (30%)",
    "Remaining": "7 (70%)"
}
print(compact_panel(stats, title="Progress"))
```

## Testing

Run the test suite to verify cross-platform compatibility:

```bash
cd claude-terminal-ui
python test_new_components.py
```

See `examples/session_display.py` for a comprehensive example.

## API Consistency

These components follow the same patterns as existing components:

1. **Capability Detection**: Automatic Unicode/ASCII fallback
2. **Color Support**: Optional color parameters with graceful degradation
3. **Type Hints**: Full type annotations for all functions
4. **Documentation**: Comprehensive docstrings with examples
5. **Formatting**: Consistent indentation, prefix, and width parameters

## Integration

Import from `claude_terminal_ui.components`:

```python
from claude_terminal_ui.components import (
    tree, nested_list, simple_tree, TreeNode,
    panel, box, info_panel, titled_box, compact_panel
)
```

All functions are re-exported in the main components module.
