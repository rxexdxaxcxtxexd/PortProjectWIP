#!/usr/bin/env python3
"""
Example: Session Checkpoint Display

Demonstrates using trees and panels to create a session checkpoint
display similar to resume-session.py but using claude-terminal-ui.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from claude_terminal_ui.components.trees import tree, simple_tree, TreeNode
from claude_terminal_ui.components.panels import panel, compact_panel, titled_box
from claude_terminal_ui.components.headers import header, divider
from claude_terminal_ui.components.status import success, warning, info
from claude_terminal_ui.tokens.colors import Colors


def display_session_checkpoint():
    """Display a complete session checkpoint"""

    # Header
    print(header("SESSION CHECKPOINT", color=Colors.INFO))
    print()

    # Session metadata in a compact panel
    session_data = {
        "Session ID": "5150ba34",
        "Started": "2025-12-30 12:49:35",
        "Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Duration": "2h 15m",
    }
    print(compact_panel(session_data, title="Session Info", color=Colors.INFO))
    print()

    # Project information
    project_data = {
        "Name": "claude-terminal-ui",
        "Path": "C:\\Users\\layden\\Portfolio-Analysis\\claude-terminal-ui",
        "Branch": "main",
        "Status": "Clean",
    }
    print(compact_panel(project_data, title="Project", color=Colors.ACCENT))
    print()

    # Resume points as a tree
    print(info("Resume Points"))
    print()
    resume_root = TreeNode(
        "Tasks",
        children=[
            TreeNode("In Progress", children=[TreeNode("Implement tree and panel components")]),
            TreeNode(
                "Next (3)",
                children=[
                    TreeNode("Write comprehensive tests"),
                    TreeNode("Update documentation"),
                    TreeNode("Create usage examples"),
                ],
            ),
        ],
    )
    print(tree(resume_root, indent=2))
    print()

    # Recent changes in a titled box
    recent_changes = [
        "Added trees.py component",
        "Added panels.py component",
        "Updated __init__.py exports",
        "Created test_new_components.py",
    ]
    print(titled_box(recent_changes, title="Recent Changes", color=Colors.SUCCESS))
    print()

    # Next steps
    next_steps = [
        "Run full test suite",
        "Verify cross-platform compatibility",
        "Review code for edge cases",
        "Update package documentation",
    ]
    print(titled_box(next_steps, title="Next Steps", color=Colors.WARNING))
    print()

    # Footer with status messages
    print(divider())
    print(success("All components implemented successfully"))
    print(info("Tests passing with ASCII fallback"))
    print(warning("Run additional tests on Unix systems for Unicode support"))
    print()


def display_file_tree():
    """Display a file tree structure"""
    print(header("PROJECT STRUCTURE", color=Colors.ACCENT))
    print()

    # Build a tree of project files
    project_root = TreeNode(
        "claude-terminal-ui/",
        children=[
            TreeNode(
                "src/",
                children=[
                    TreeNode(
                        "claude_terminal_ui/",
                        children=[
                            TreeNode("components/", color=Colors.INFO),
                            TreeNode("core/", color=Colors.INFO),
                            TreeNode("tokens/", color=Colors.INFO),
                            TreeNode("themes/", color=Colors.MUTED),
                        ],
                    )
                ],
            ),
            TreeNode(
                "tests/",
                children=[
                    TreeNode("test_components.py", color=Colors.SUCCESS),
                    TreeNode("test_capabilities.py", color=Colors.SUCCESS),
                ],
            ),
            TreeNode(
                "examples/",
                children=[
                    TreeNode("session_display.py", color=Colors.HIGHLIGHT),
                ],
            ),
        ],
    )

    print(tree(project_root))
    print()


def display_task_progress():
    """Display task progress with trees and panels"""
    print(header("TASK PROGRESS", color=Colors.SUCCESS))
    print()

    # Completed tasks
    completed_tasks = [
        "Design component API",
        "Implement tree() function",
        "Implement nested_list() function",
        "Implement panel() function",
        "Implement box() function",
        "Add color support",
    ]
    print(titled_box(completed_tasks, title="Completed (6)", color=Colors.SUCCESS))
    print()

    # In progress
    in_progress = TreeNode(
        "Current Task",
        children=[
            TreeNode("Testing components", color=Colors.WARNING),
            TreeNode(
                "Subtasks",
                children=[
                    TreeNode("Test ASCII fallback - Done", color=Colors.SUCCESS),
                    TreeNode("Test Unicode mode - Pending", color=Colors.WARNING),
                    TreeNode("Test colors - Done", color=Colors.SUCCESS),
                ],
            ),
        ],
    )
    print(tree(in_progress, indent=2))
    print()

    # Statistics panel
    stats = {
        "Total Tasks": "12",
        "Completed": "6 (50%)",
        "In Progress": "3 (25%)",
        "Remaining": "3 (25%)",
    }
    print(compact_panel(stats, title="Statistics", color=Colors.INFO))
    print()


if __name__ == "__main__":
    # Display different examples
    display_session_checkpoint()
    print()
    print("=" * 70)
    print()
    display_file_tree()
    print()
    print("=" * 70)
    print()
    display_task_progress()
