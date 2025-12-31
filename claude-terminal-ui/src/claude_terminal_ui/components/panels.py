"""
Panel and Box Components

Boxed content components for terminal output:
- panel() - Content in a bordered box with optional title
- box() - Simple border box around content
- info_panel() - Informational panel with icon

Example panel output:
    ┌────────────────────────┐
    │ Session Checkpoint     │
    │ ID: 5150ba34          │
    └────────────────────────┘
"""

from typing import Optional, List
from ..core.capabilities import get_capabilities
from ..tokens.colors import Color, Colors, RESET, Styles
from ..tokens.symbols import Symbols
from ..tokens.spacing import DEFAULT_WIDTH


def panel(
    content: str,
    *,
    title: Optional[str] = None,
    width: Optional[int] = None,
    color: Optional[Color] = None,
    title_color: Optional[Color] = None,
    padding: int = 1,
    align: str = "left",
) -> str:
    """
    Create a panel with bordered content.

    Args:
        content: Text content to display in the panel
        title: Optional title displayed at the top
        width: Panel width (auto-sized if None)
        color: Border color
        title_color: Title color (defaults to color if not specified)
        padding: Internal padding (spaces)
        align: Content alignment ("left", "center", "right")

    Returns:
        Formatted panel string with borders

    Example:
        >>> print(panel("Hello World", title="Greeting"))
        ┌─ Greeting ──────┐
        │ Hello World     │
        └─────────────────┘
    """
    caps = get_capabilities()

    # Get box drawing characters
    tl = Symbols.BOX_TOP_LEFT.render()
    tr = Symbols.BOX_TOP_RIGHT.render()
    bl = Symbols.BOX_BOTTOM_LEFT.render()
    br = Symbols.BOX_BOTTOM_RIGHT.render()
    h = Symbols.BOX_HORIZONTAL.render()
    v = Symbols.BOX_VERTICAL.render()

    # Split content into lines
    content_lines = content.split("\n")

    # Calculate width
    if width is None:
        # Auto-size based on content
        max_content_width = max(len(line) for line in content_lines) if content_lines else 0
        title_width = len(title) + 4 if title else 0  # "─ Title ─"
        width = max(max_content_width + (padding * 2) + 2, title_width + 4, 20)

    inner_width = width - 2  # Account for side borders

    # Apply colors if supported
    border_color_code = ""
    title_color_code = ""
    reset_code = ""

    if caps.color_support.value > 0:
        if color:
            border_color_code = color.code()
            reset_code = RESET
        if title_color:
            title_color_code = title_color.code()
        elif color:
            title_color_code = color.code()

    # Build top border with optional title
    if title:
        title_section = f"{h} {title} "
        remaining_width = inner_width - len(title_section)
        if remaining_width < 0:
            remaining_width = 0
        top_border = (
            f"{border_color_code}{tl}{title_section}"
            f"{h * remaining_width}{tr}{reset_code}"
        )
    else:
        top_border = f"{border_color_code}{tl}{h * inner_width}{tr}{reset_code}"

    # Build content lines
    panel_lines = [top_border]

    for line in content_lines:
        # Apply alignment
        line_len = len(line)
        available_width = inner_width - (padding * 2)

        if align == "center":
            left_padding = (available_width - line_len) // 2
            right_padding = available_width - line_len - left_padding
            padded_line = (
                " " * padding + " " * left_padding + line + " " * right_padding + " " * padding
            )
        elif align == "right":
            left_padding = available_width - line_len
            padded_line = " " * padding + " " * left_padding + line + " " * padding
        else:  # left
            right_padding = available_width - line_len
            if right_padding < 0:
                # Line is too long, truncate it
                line = line[: available_width - 3] + "..."
                right_padding = 0
            padded_line = " " * padding + line + " " * right_padding + " " * padding

        # Ensure consistent width
        if len(padded_line) < inner_width:
            padded_line += " " * (inner_width - len(padded_line))
        elif len(padded_line) > inner_width:
            padded_line = padded_line[:inner_width]

        panel_lines.append(f"{border_color_code}{v}{reset_code}{padded_line}{border_color_code}{v}{reset_code}")

    # Build bottom border
    bottom_border = f"{border_color_code}{bl}{h * inner_width}{br}{reset_code}"
    panel_lines.append(bottom_border)

    return "\n".join(panel_lines)


def box(
    content: str,
    *,
    width: Optional[int] = None,
    color: Optional[Color] = None,
    padding: int = 1,
) -> str:
    """
    Create a simple box around content (no title).

    Args:
        content: Text content to display
        width: Box width (auto-sized if None)
        color: Border color
        padding: Internal padding (spaces)

    Returns:
        Formatted box string

    Example:
        >>> print(box("Important"))
        ┌───────────┐
        │ Important │
        └───────────┘
    """
    return panel(content, width=width, color=color, padding=padding)


def info_panel(
    message: str,
    *,
    title: Optional[str] = None,
    width: Optional[int] = None,
    panel_type: str = "info",
) -> str:
    """
    Create an informational panel with appropriate icon and color.

    Args:
        message: Message to display
        title: Optional panel title
        width: Panel width
        panel_type: Type of panel ("info", "success", "warning", "error")

    Returns:
        Formatted panel with icon and appropriate color

    Example:
        >>> print(info_panel("Task completed", panel_type="success"))
        ┌─────────────────┐
        │ ✓ Task completed │
        └─────────────────┘
    """
    # Map panel types to colors and symbols
    type_config = {
        "info": (Colors.INFO, Symbols.INFO),
        "success": (Colors.SUCCESS, Symbols.SUCCESS),
        "warning": (Colors.WARNING, Symbols.WARNING),
        "error": (Colors.ERROR, Symbols.ERROR),
        "debug": (Colors.DEBUG, Symbols.DEBUG),
    }

    color, symbol = type_config.get(panel_type, (Colors.INFO, Symbols.INFO))

    # Add symbol to message
    symbol_str = symbol.render()
    content = f"{symbol_str} {message}"

    return panel(content, title=title, width=width, color=color)


def titled_box(
    items: List[str],
    *,
    title: str,
    width: Optional[int] = None,
    color: Optional[Color] = None,
    bullet: str = "•",
) -> str:
    """
    Create a box with a title and list of items.

    Args:
        items: List of items to display
        title: Box title
        width: Box width
        color: Border and title color
        bullet: Bullet character for items

    Returns:
        Formatted box with title and items

    Example:
        >>> print(titled_box(["Item 1", "Item 2"], title="Tasks"))
        ┌─ Tasks ─────────┐
        │ • Item 1        │
        │ • Item 2        │
        └─────────────────┘
    """
    caps = get_capabilities()

    # Resolve bullet
    if bullet == "•":
        bullet_char = Symbols.BULLET.render()
    else:
        bullet_char = bullet

    # Build content
    content_lines = [f"{bullet_char} {item}" for item in items]
    content = "\n".join(content_lines)

    return panel(content, title=title, width=width, color=color)


def compact_panel(
    key_values: dict,
    *,
    title: Optional[str] = None,
    width: Optional[int] = None,
    color: Optional[Color] = None,
) -> str:
    """
    Create a compact panel displaying key-value pairs.

    Args:
        key_values: Dictionary of key-value pairs to display
        title: Optional panel title
        width: Panel width
        color: Border color

    Returns:
        Formatted panel with key-value pairs

    Example:
        >>> data = {"ID": "5150ba34", "Status": "Active"}
        >>> print(compact_panel(data, title="Session"))
        ┌─ Session ───────┐
        │ ID: 5150ba34    │
        │ Status: Active  │
        └─────────────────┘
    """
    # Find max key length for alignment
    max_key_len = max(len(str(k)) for k in key_values.keys()) if key_values else 0

    # Build content lines
    content_lines = []
    for key, value in key_values.items():
        padded_key = str(key).ljust(max_key_len)
        content_lines.append(f"{padded_key}: {value}")

    content = "\n".join(content_lines)

    return panel(content, title=title, width=width, color=color)
