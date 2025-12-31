"""
Tree and Nested List Components

Hierarchical display components for terminal output:
- tree() - Tree structure with branches
- nested_list() - Indented nested lists

Example tree output:
    🎯 Resume Points
    ├── In Progress
    │   └── Fix authentication bug
    └── Next (3)
        ├── Run tests
        ├── Build project
        └── Deploy
"""

from typing import List, Optional, Union
from ..core.capabilities import get_capabilities
from ..tokens.colors import Color, Colors, RESET
from ..tokens.symbols import Symbols


class TreeNode:
    """Represents a node in a tree structure"""

    def __init__(
        self,
        label: str,
        children: Optional[List["TreeNode"]] = None,
        color: Optional[Color] = None,
    ):
        """
        Create a tree node.

        Args:
            label: The text to display for this node
            children: Optional list of child nodes
            color: Optional color to apply to the label
        """
        self.label = label
        self.children = children or []
        self.color = color


def tree(
    root: Union[TreeNode, str],
    *,
    indent: int = 0,
    prefix: str = "",
    color: Optional[Color] = None,
) -> str:
    """
    Create a tree structure with branches.

    Args:
        root: Either a TreeNode or a string label for the root
        indent: Initial indentation level (spaces)
        prefix: Prefix string for each line
        color: Default color for nodes without explicit colors

    Returns:
        Formatted tree string with Unicode box-drawing characters

    Example:
        >>> node = TreeNode("Files", [
        ...     TreeNode("src"),
        ...     TreeNode("tests"),
        ... ])
        >>> print(tree(node))
        Files
        ├── src
        └── tests
    """
    caps = get_capabilities()

    # Convert string to TreeNode if needed
    if isinstance(root, str):
        root = TreeNode(root)

    lines = []

    # Render root node
    indent_str = " " * indent
    node_color = root.color or color
    if node_color and caps.color_support.value > 0:
        root_label = f"{node_color.code()}{root.label}{RESET}"
    else:
        root_label = root.label

    lines.append(f"{prefix}{indent_str}{root_label}")

    # Render children
    if root.children:
        _render_tree_children(
            root.children,
            lines,
            prefix=prefix,
            indent=indent,
            parent_prefix="",
            caps=caps,
            default_color=color,
        )

    return "\n".join(lines)


def _render_tree_children(
    children: List[TreeNode],
    lines: List[str],
    prefix: str,
    indent: int,
    parent_prefix: str,
    caps,
    default_color: Optional[Color] = None,
) -> None:
    """Helper to recursively render tree children"""
    for i, child in enumerate(children):
        is_last = i == len(children) - 1

        # Choose branch symbol
        if is_last:
            branch = Symbols.TREE_LAST.render()
            continuation = Symbols.TREE_SPACE.render()
        else:
            branch = Symbols.TREE_BRANCH.render()
            continuation = Symbols.TREE_PIPE.render() + "  "

        # Render child label
        child_color = child.color or default_color
        if child_color and caps.color_support.value > 0:
            child_label = f"{child_color.code()}{child.label}{RESET}"
        else:
            child_label = child.label

        indent_str = " " * indent
        line = f"{prefix}{indent_str}{parent_prefix}{branch} {child_label}"
        lines.append(line)

        # Render grandchildren
        if child.children:
            _render_tree_children(
                child.children,
                lines,
                prefix=prefix,
                indent=indent,
                parent_prefix=parent_prefix + continuation,
                caps=caps,
                default_color=default_color,
            )


def nested_list(
    items: List[Union[str, tuple]],
    *,
    indent: int = 0,
    bullet: str = "•",
    prefix: str = "",
    color: Optional[Color] = None,
    level_indent: int = 2,
) -> str:
    """
    Create an indented nested list.

    Args:
        items: List of items. Each item can be:
               - str: Simple item
               - tuple: (label, List[items]) for nested structure
        indent: Initial indentation level (spaces)
        bullet: Bullet character to use
        prefix: Prefix string for each line
        color: Optional color for items
        level_indent: Spaces per nesting level

    Returns:
        Formatted nested list string

    Example:
        >>> items = [
        ...     "First item",
        ...     ("Nested", ["Child 1", "Child 2"]),
        ...     "Last item"
        ... ]
        >>> print(nested_list(items))
        • First item
        • Nested
          • Child 1
          • Child 2
        • Last item
    """
    caps = get_capabilities()

    # Resolve bullet symbol
    if bullet == "•":
        bullet_char = Symbols.BULLET.render()
    else:
        bullet_char = bullet

    lines = []
    indent_str = " " * indent

    for item in items:
        if isinstance(item, tuple):
            # Nested structure
            label, children = item
            if color and caps.color_support.value > 0:
                label_text = f"{color.code()}{label}{RESET}"
            else:
                label_text = label

            lines.append(f"{prefix}{indent_str}{bullet_char} {label_text}")

            # Recursively render children
            if children:
                child_output = nested_list(
                    children,
                    indent=indent + level_indent,
                    bullet=bullet,
                    prefix=prefix,
                    color=color,
                    level_indent=level_indent,
                )
                lines.append(child_output)
        else:
            # Simple item
            if color and caps.color_support.value > 0:
                item_text = f"{color.code()}{item}{RESET}"
            else:
                item_text = item

            lines.append(f"{prefix}{indent_str}{bullet_char} {item_text}")

    return "\n".join(lines)


def simple_tree(
    items: List[str],
    *,
    title: Optional[str] = None,
    indent: int = 0,
    prefix: str = "",
    color: Optional[Color] = None,
) -> str:
    """
    Create a simple tree from a flat list of items.

    Args:
        items: List of item labels
        title: Optional title for the tree
        indent: Initial indentation level
        prefix: Prefix string for each line
        color: Optional color for items

    Returns:
        Formatted tree string

    Example:
        >>> print(simple_tree(["item1", "item2"], title="Tasks"))
        Tasks
        ├── item1
        └── item2
    """
    if not items:
        return ""

    # Build tree nodes
    children = [TreeNode(item) for item in items]

    if title:
        root = TreeNode(title, children=children, color=color)
    else:
        # No title, just render items as a flat tree
        caps = get_capabilities()
        lines = []
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            branch = Symbols.TREE_LAST.render() if is_last else Symbols.TREE_BRANCH.render()

            if color and caps.color_support.value > 0:
                item_text = f"{color.code()}{item}{RESET}"
            else:
                item_text = item

            indent_str = " " * indent
            lines.append(f"{prefix}{indent_str}{branch} {item_text}")

        return "\n".join(lines)

    return tree(root, indent=indent, prefix=prefix)
