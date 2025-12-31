#!/usr/bin/env python3
"""
Test script to demonstrate Unicode rendering.
Forces Unicode mode to show the difference.
"""

import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from claude_terminal_ui.components.trees import tree, TreeNode
from claude_terminal_ui.components.panels import panel, compact_panel
from claude_terminal_ui.tokens.colors import Colors


def test_unicode_vs_ascii():
    """Show both Unicode and ASCII rendering"""

    # Create a tree structure
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
                ],
            ),
        ],
    )

    print("=" * 70)
    print("UNICODE VS ASCII COMPARISON")
    print("=" * 70)
    print()

    print("ASCII Mode (Current):")
    print("-" * 70)
    print(tree(root))
    print()

    print("Unicode Mode (Example - if terminal supported it):")
    print("-" * 70)
    # Show what it would look like with Unicode (as description)
    print("Resume Points")
    print("[tree-branch] In Progress")
    print("[tree-pipe]   [tree-last] Fix authentication bug")
    print("[tree-last] Next (3)")
    print("    [tree-branch] Run tests")
    print("    [tree-last] Build project")
    print()
    print("(Unicode box-drawing characters would be used instead of |, `, -)")
    print()

    # Panel comparison
    session_info = {
        "Session ID": "5150ba34",
        "Status": "Active",
    }

    print("Panel - ASCII Mode:")
    print("-" * 70)
    print(panel("Session Checkpoint", title="Info"))
    print()

    print("Panel - Unicode Mode (Example - if terminal supported it):")
    print("-" * 70)
    print("Would use box-drawing characters instead of +, -, |")
    print()


if __name__ == "__main__":
    test_unicode_vs_ascii()
