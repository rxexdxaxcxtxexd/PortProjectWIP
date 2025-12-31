#!/usr/bin/env python3
"""
Test script for new tree and panel components.
Tests both Unicode and ASCII fallback rendering.
"""

import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from claude_terminal_ui.components.trees import tree, nested_list, simple_tree, TreeNode
from claude_terminal_ui.components.panels import (
    panel,
    box,
    info_panel,
    titled_box,
    compact_panel,
)
from claude_terminal_ui.tokens.colors import Colors
from claude_terminal_ui.core.capabilities import get_capabilities


def test_trees():
    """Test tree components"""
    print("=" * 70)
    print("TREE COMPONENTS TEST")
    print("=" * 70)
    print()

    # Test 1: Simple tree with TreeNode
    print("Test 1: Simple Tree with TreeNode")
    print("-" * 70)
    root = TreeNode(
        "Resume Points",
        children=[
            TreeNode(
                "In Progress",
                children=[TreeNode("Fix authentication bug")],
            ),
            TreeNode(
                "Next (3)",
                children=[
                    TreeNode("Run tests"),
                    TreeNode("Build project"),
                    TreeNode("Deploy"),
                ],
            ),
        ],
    )
    print(tree(root))
    print()

    # Test 2: Simple tree from list
    print("Test 2: Simple Tree from List")
    print("-" * 70)
    items = ["First item", "Second item", "Third item"]
    print(simple_tree(items, title="Tasks"))
    print()

    # Test 3: Nested list
    print("Test 3: Nested List")
    print("-" * 70)
    nested_items = [
        "Top level item",
        ("Nested section", ["Child 1", "Child 2"]),
        "Another top level",
    ]
    print(nested_list(nested_items))
    print()

    # Test 4: Colored tree (if supported)
    print("Test 4: Colored Tree")
    print("-" * 70)
    colored_root = TreeNode(
        "Project Files",
        children=[
            TreeNode("src/", color=Colors.INFO),
            TreeNode("tests/", color=Colors.SUCCESS),
            TreeNode("docs/", color=Colors.MUTED),
        ],
    )
    print(tree(colored_root))
    print()


def test_panels():
    """Test panel components"""
    print("=" * 70)
    print("PANEL COMPONENTS TEST")
    print("=" * 70)
    print()

    # Test 1: Basic panel
    print("Test 1: Basic Panel")
    print("-" * 70)
    print(panel("Hello World", title="Greeting"))
    print()

    # Test 2: Simple box
    print("Test 2: Simple Box")
    print("-" * 70)
    print(box("Important message"))
    print()

    # Test 3: Info panels of different types
    print("Test 3: Info Panels")
    print("-" * 70)
    print(info_panel("Task completed successfully", panel_type="success"))
    print()
    print(info_panel("Warning: Low disk space", panel_type="warning"))
    print()
    print(info_panel("Error: Connection failed", panel_type="error"))
    print()
    print(info_panel("Processing data...", panel_type="info"))
    print()

    # Test 4: Titled box with items
    print("Test 4: Titled Box with Items")
    print("-" * 70)
    tasks = ["Run tests", "Build project", "Deploy to production"]
    print(titled_box(tasks, title="Next Steps", color=Colors.INFO))
    print()

    # Test 5: Compact panel with key-value pairs
    print("Test 5: Compact Panel")
    print("-" * 70)
    session_data = {
        "ID": "5150ba34",
        "Status": "Active",
        "Started": "2025-12-30 14:30",
        "Tasks": "3 pending",
    }
    print(compact_panel(session_data, title="Session Info", color=Colors.ACCENT))
    print()

    # Test 6: Multi-line content
    print("Test 6: Multi-line Panel")
    print("-" * 70)
    multiline = "Line 1\nLine 2\nLine 3"
    print(panel(multiline, title="Multiple Lines"))
    print()

    # Test 7: Centered and right-aligned
    print("Test 7: Aligned Content")
    print("-" * 70)
    print(panel("Centered", align="center", width=40))
    print()
    print(panel("Right", align="right", width=40))
    print()


def test_combined():
    """Test combining trees and panels"""
    print("=" * 70)
    print("COMBINED COMPONENTS TEST")
    print("=" * 70)
    print()

    # Create a session checkpoint display
    print("Session Checkpoint Display")
    print("-" * 70)

    # Session info in a panel
    session_info = {
        "Session ID": "5150ba34",
        "Started": "2025-12-30 14:30:00",
        "Status": "In Progress",
    }
    print(compact_panel(session_info, title="Session Checkpoint", color=Colors.INFO))
    print()

    # Resume points as a tree
    resume_root = TreeNode(
        "Resume Points",
        children=[
            TreeNode("Continue work on API documentation"),
            TreeNode("Run comprehensive tests"),
        ],
    )
    print(tree(resume_root, prefix="  "))
    print()

    # Next steps in a titled box
    next_steps = [
        "Write tests for new code",
        "Review newly created files",
        "Verify all changes work",
    ]
    print(titled_box(next_steps, title="Next Steps", color=Colors.WARNING))
    print()


def print_capabilities():
    """Print terminal capabilities"""
    caps = get_capabilities()
    print("=" * 70)
    print("TERMINAL CAPABILITIES")
    print("=" * 70)
    print(f"Terminal: {caps.terminal_name}")
    print(f"Platform: {'Windows' if caps.is_windows else 'Unix-like'}")
    print(f"Color Support: {caps.color_support.name} ({caps.color_support.value} colors)")
    print(f"Unicode Support: {'Yes' if caps.unicode_support else 'No (ASCII fallback)'}")
    print(f"Dimensions: {caps.width}x{caps.height}")
    print(f"Interactive: {'Yes' if caps.is_interactive else 'No'}")
    print(f"Hyperlinks: {'Supported' if caps.supports_hyperlinks else 'Not supported'}")
    print()


if __name__ == "__main__":
    print_capabilities()
    test_trees()
    test_panels()
    test_combined()

    print("=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
