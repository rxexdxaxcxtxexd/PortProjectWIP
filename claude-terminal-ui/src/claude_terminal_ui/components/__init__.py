"""UI components for terminal output."""

from .status import (
    success,
    error,
    warning,
    info,
    debug,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_debug,
)
from .headers import header, subheader, divider, step_header
from .progress import progress_bar, Spinner, spinner, step_indicator
from .tables import (
    key_value,
    table,
    stats_panel,
    print_key_value,
    print_table,
    print_stats_panel,
)
from .trees import tree, nested_list, simple_tree, TreeNode
from .panels import (
    panel,
    box,
    info_panel,
    titled_box,
    compact_panel,
)

__all__ = [
    # Status messages
    "success",
    "error",
    "warning",
    "info",
    "debug",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_debug",
    # Headers
    "header",
    "subheader",
    "divider",
    "step_header",
    # Progress
    "progress_bar",
    "Spinner",
    "spinner",
    "step_indicator",
    # Tables
    "key_value",
    "table",
    "stats_panel",
    "print_key_value",
    "print_table",
    "print_stats_panel",
    # Trees
    "tree",
    "nested_list",
    "simple_tree",
    "TreeNode",
    # Panels
    "panel",
    "box",
    "info_panel",
    "titled_box",
    "compact_panel",
]
