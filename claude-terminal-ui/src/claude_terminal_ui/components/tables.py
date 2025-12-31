"""
Table Formatting Components

Provides consistent table formatting with:
- key_value(): Format key-value pairs
- table(): Full data tables with headers
- stats_panel(): Statistics summary panels
"""

from typing import Any, Dict, List, Optional, Union
from ..core.capabilities import get_capabilities
from ..tokens.colors import Colors, RESET, Styles, Color
from ..tokens.spacing import DEFAULT_WIDTH, WIDE_WIDTH, CELL_PADDING


def _get_box_chars(unicode_supported: bool) -> Dict[str, str]:
    """Get box-drawing characters based on unicode support"""
    if unicode_supported:
        return {
            'horizontal': '─',
            'vertical': '│',
            'top_left': '┌',
            'top_right': '┐',
            'bottom_left': '└',
            'bottom_right': '┘',
            'cross': '┼',
            'tee_down': '┬',
            'tee_up': '┴',
            'tee_right': '├',
            'tee_left': '┤',
        }
    else:
        return {
            'horizontal': '-',
            'vertical': '|',
            'top_left': '+',
            'top_right': '+',
            'bottom_left': '+',
            'bottom_right': '+',
            'cross': '+',
            'tee_down': '+',
            'tee_up': '+',
            'tee_right': '+',
            'tee_left': '+',
        }


def key_value(
    items: Dict[str, Any],
    *,
    width: int = DEFAULT_WIDTH,
    indent: int = 0,
    align_colon: bool = True,
    value_color: Optional[Color] = None,
    key_width: Optional[int] = None,
) -> str:
    """
    Format key-value pairs with aligned colons.

    Example output:
      Session:  5150ba34
      Started:  2025-12-29 12:49
      Tokens:   1,234 / 200,000

    Args:
        items: Dictionary of key-value pairs to format
        width: Total width for output
        indent: Left indentation in spaces
        align_colon: If True, align all colons at same column
        value_color: Optional color for values
        key_width: Fixed width for keys (auto-calculated if None)

    Returns:
        Formatted string with key-value pairs
    """
    caps = get_capabilities()
    indent_str = " " * indent

    # Convert all values to strings
    str_items = {k: str(v) for k, v in items.items()}

    # Calculate key width for alignment
    if key_width is None:
        key_width = max(len(k) for k in str_items.keys()) if str_items else 0

    lines = []
    for key, value in str_items.items():
        if align_colon:
            # Align colons at same column
            padding = " " * (key_width - len(key))
            formatted_key = f"{key}{padding}:"
        else:
            formatted_key = f"{key}:"

        # Apply color to value if supported and specified
        if value_color and caps.color_support.value > 0:
            formatted_value = f"{value_color.code()}{value}{RESET}"
        else:
            formatted_value = value

        lines.append(f"{indent_str}{formatted_key} {formatted_value}")

    return "\n".join(lines)


def table(
    data: List[List[str]],
    headers: Optional[List[str]] = None,
    *,
    width: int = DEFAULT_WIDTH,
    align: Optional[List[str]] = None,
    header_color: Optional[Color] = None,
    show_borders: bool = True,
    compact: bool = False,
) -> str:
    """
    Format a full data table with optional headers and borders.

    Example output:
    +----------+--------+--------+
    | Key      | Status | Count  |
    +----------+--------+--------+
    | BOPS-123 | Done   | 5      |
    | BOPS-124 | Active | 12     |
    +----------+--------+--------+

    Args:
        data: List of rows, each row is a list of cell values
        headers: Optional header row
        width: Maximum table width (may be exceeded for wide content)
        align: List of alignment specifiers ('left', 'right', 'center') per column
        header_color: Optional color for header text
        show_borders: If True, show table borders and dividers
        compact: If True, use minimal spacing (no padding)

    Returns:
        Formatted table string
    """
    if not data and not headers:
        return ""

    caps = get_capabilities()
    box = _get_box_chars(caps.unicode_support)

    # Determine number of columns
    num_cols = len(headers) if headers else len(data[0]) if data else 0
    if num_cols == 0:
        return ""

    # Combine headers and data for width calculation
    all_rows = []
    if headers:
        all_rows.append(headers)
    all_rows.extend(data)

    # Calculate column widths
    col_widths = []
    for col_idx in range(num_cols):
        max_width = 0
        for row in all_rows:
            if col_idx < len(row):
                cell_text = str(row[col_idx])
                max_width = max(max_width, len(cell_text))
        col_widths.append(max_width)

    # Default alignment is left
    if align is None:
        align = ['left'] * num_cols
    else:
        # Pad alignment list if needed
        align = align + ['left'] * (num_cols - len(align))

    # Cell padding
    padding = 0 if compact else CELL_PADDING

    def format_cell(text: str, width: int, alignment: str) -> str:
        """Format a cell with padding and alignment"""
        text = str(text)
        if alignment == 'right':
            return text.rjust(width + padding * 2)
        elif alignment == 'center':
            return text.center(width + padding * 2)
        else:  # left
            return text.ljust(width + padding * 2)

    def make_border(style: str) -> str:
        """Create a border line"""
        if not show_borders:
            return ""

        if style == 'top':
            left = box['top_left']
            right = box['top_right']
            sep = box['tee_down']
        elif style == 'middle':
            left = box['tee_right']
            right = box['tee_left']
            sep = box['cross']
        else:  # bottom
            left = box['bottom_left']
            right = box['bottom_right']
            sep = box['tee_up']

        segments = [box['horizontal'] * (w + padding * 2) for w in col_widths]
        return left + sep.join(segments) + right

    def make_row(row_data: List[str], is_header: bool = False) -> str:
        """Create a data row"""
        cells = []
        for col_idx, cell_text in enumerate(row_data):
            if col_idx < len(col_widths):
                width = col_widths[col_idx]
                alignment = align[col_idx]
                formatted = format_cell(cell_text, width, alignment)

                # Apply header styling if needed
                if is_header:
                    if caps.color_support.value > 0:
                        if header_color:
                            formatted = f"{header_color.code()}{formatted}{RESET}"
                        else:
                            formatted = f"{Styles.BOLD}{formatted}{RESET}"

                cells.append(formatted)

        if show_borders:
            return box['vertical'] + box['vertical'].join(cells) + box['vertical']
        else:
            return " ".join(cells)

    # Build table
    lines = []

    # Top border
    if show_borders:
        lines.append(make_border('top'))

    # Header row
    if headers:
        lines.append(make_row(headers, is_header=True))
        if show_borders:
            lines.append(make_border('middle'))

    # Data rows
    for row in data:
        lines.append(make_row(row))

    # Bottom border
    if show_borders:
        lines.append(make_border('bottom'))

    return "\n".join(lines)


def stats_panel(
    stats: Dict[str, Any],
    *,
    title: Optional[str] = None,
    width: int = DEFAULT_WIDTH,
    layout: str = "grid",
    columns: int = 2,
    show_borders: bool = True,
    title_color: Optional[Color] = None,
) -> str:
    """
    Format a statistics summary panel.

    Example output (grid layout):
    ┌──────────────────────────────────────┐
    │         STATISTICS SUMMARY           │
    ├──────────────────────────────────────┤
    │ Total:      100    Active:      25   │
    │ Complete:    70    Pending:      5   │
    └──────────────────────────────────────┘

    Example output (list layout):
    STATISTICS SUMMARY
    ------------------
      Total:      100
      Active:      25
      Complete:    70
      Pending:      5

    Args:
        stats: Dictionary of statistics to display
        title: Optional panel title
        width: Panel width
        layout: Layout style - "grid" (multi-column) or "list" (single column)
        columns: Number of columns for grid layout
        show_borders: If True, show panel borders
        title_color: Optional color for title text

    Returns:
        Formatted statistics panel string
    """
    caps = get_capabilities()
    box = _get_box_chars(caps.unicode_support)

    if layout == "list":
        # Simple list layout
        lines = []

        if title:
            if show_borders:
                lines.append("─" * width if caps.unicode_support else "-" * width)
            if title_color and caps.color_support.value > 0:
                title_line = f"{title_color.code()}{title}{RESET}"
            else:
                title_line = title
            lines.append(title_line)
            if show_borders:
                lines.append("─" * width if caps.unicode_support else "-" * width)

        # Format as key-value list
        lines.append(key_value(stats, width=width, indent=2))

        return "\n".join(lines)

    else:  # grid layout
        lines = []
        content_width = width - 4  # Account for borders and padding

        # Top border with title
        if show_borders:
            lines.append(box['top_left'] + box['horizontal'] * (width - 2) + box['top_right'])

            if title:
                # Center title
                title_text = f" {title} " if title else ""
                if title_color and caps.color_support.value > 0:
                    title_text = f"{title_color.code()}{title_text}{RESET}"
                padded_title = title_text.center(width - 2)
                lines.append(box['vertical'] + padded_title + box['vertical'])
                lines.append(box['tee_right'] + box['horizontal'] * (width - 2) + box['tee_left'])

        # Calculate column width for grid
        col_width = content_width // columns

        # Convert stats to list of items
        items = list(stats.items())

        # Process items in grid format
        for i in range(0, len(items), columns):
            row_items = items[i:i + columns]
            row_parts = []

            for key, value in row_items:
                # Format as "Key: Value"
                item_text = f"{key}: {value}"
                row_parts.append(item_text.ljust(col_width))

            # Combine row parts
            row_content = "".join(row_parts)

            # Truncate if too long
            if len(row_content) > content_width:
                row_content = row_content[:content_width - 3] + "..."

            # Pad to full width
            row_content = row_content.ljust(content_width)

            if show_borders:
                lines.append(box['vertical'] + " " + row_content + " " + box['vertical'])
            else:
                lines.append(row_content)

        # Bottom border
        if show_borders:
            lines.append(box['bottom_left'] + box['horizontal'] * (width - 2) + box['bottom_right'])

        return "\n".join(lines)


# Print variants that output directly
def print_key_value(items: Dict[str, Any], **kwargs) -> None:
    """Print key-value pairs"""
    print(key_value(items, **kwargs))


def print_table(data: List[List[str]], headers: Optional[List[str]] = None, **kwargs) -> None:
    """Print formatted table"""
    print(table(data, headers, **kwargs))


def print_stats_panel(stats: Dict[str, Any], **kwargs) -> None:
    """Print statistics panel"""
    print(stats_panel(stats, **kwargs))
