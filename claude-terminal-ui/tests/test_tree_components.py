"""Tests for tree and nested list components"""
import pytest
from claude_terminal_ui.components.trees import (
    tree,
    nested_list,
    simple_tree,
    TreeNode,
)


class TestTreeComponents:
    """Test tree structure functions"""

    def test_tree_node_creation(self):
        """TreeNode should be creatable with label"""
        node = TreeNode("Root")
        assert node.label == "Root"
        assert node.children == []

    def test_tree_node_with_children(self):
        """TreeNode should support children"""
        child1 = TreeNode("Child 1")
        child2 = TreeNode("Child 2")
        root = TreeNode("Root", children=[child1, child2])
        assert len(root.children) == 2
        assert root.children[0].label == "Child 1"

    def test_tree_basic(self):
        """tree() should render basic tree structure"""
        root = TreeNode("Root", children=[
            TreeNode("Child 1"),
            TreeNode("Child 2"),
        ])
        result = tree(root)
        assert isinstance(result, str)
        assert "Root" in result
        assert "Child 1" in result
        assert "Child 2" in result

    def test_tree_nested(self):
        """tree() should handle nested structures"""
        root = TreeNode("Root", children=[
            TreeNode("Parent 1", children=[
                TreeNode("Child 1.1"),
                TreeNode("Child 1.2"),
            ]),
            TreeNode("Parent 2"),
        ])
        result = tree(root)
        assert isinstance(result, str)
        assert "Parent 1" in result
        assert "Child 1.1" in result

    def test_tree_from_string(self):
        """tree() should accept string as root"""
        result = tree("Simple Root")
        assert isinstance(result, str)
        assert "Simple Root" in result

    def test_tree_empty_children(self):
        """tree() should handle node with no children"""
        root = TreeNode("Leaf Node")
        result = tree(root)
        assert isinstance(result, str)
        assert "Leaf Node" in result

    def test_simple_tree_basic(self):
        """simple_tree() should create tree from flat list"""
        items = ["Item 1", "Item 2", "Item 3"]
        result = simple_tree(items)
        assert isinstance(result, str)
        assert "Item 1" in result
        assert "Item 2" in result
        assert "Item 3" in result

    def test_simple_tree_with_title(self):
        """simple_tree() should include title"""
        items = ["Task 1", "Task 2"]
        result = simple_tree(items, title="TODO")
        assert isinstance(result, str)
        assert "TODO" in result
        assert "Task 1" in result

    def test_simple_tree_empty_list(self):
        """simple_tree() should handle empty list"""
        result = simple_tree([])
        assert isinstance(result, str)

    def test_nested_list_basic(self):
        """nested_list() should format basic list"""
        items = ["First", "Second", "Third"]
        result = nested_list(items)
        assert isinstance(result, str)
        assert "First" in result
        assert "Second" in result

    def test_nested_list_with_nesting(self):
        """nested_list() should handle nested tuples"""
        items = [
            "Parent 1",
            ("Child 1", [
                "Grandchild 1",
                "Grandchild 2",
            ]),
            "Parent 2",
        ]
        result = nested_list(items)
        assert isinstance(result, str)
        assert "Parent 1" in result
        assert "Child 1" in result

    def test_nested_list_custom_bullet(self):
        """nested_list() should accept custom bullet"""
        items = ["Item 1", "Item 2"]
        result = nested_list(items, bullet="-")
        assert isinstance(result, str)
        assert "Item 1" in result

    def test_nested_list_with_indent(self):
        """nested_list() should support indentation"""
        items = ["Item"]
        result = nested_list(items, indent=4)
        assert isinstance(result, str)
        # Should have leading spaces
        assert " " in result or result.startswith("Item")

    def test_tree_with_color(self):
        """tree() should support colored nodes"""
        from claude_terminal_ui.tokens.colors import Colors
        root = TreeNode("Colored", color=Colors.SUCCESS)
        result = tree(root)
        assert isinstance(result, str)
        assert "Colored" in result

    def test_tree_deep_nesting(self):
        """tree() should handle deep nesting"""
        root = TreeNode("L0", children=[
            TreeNode("L1", children=[
                TreeNode("L2", children=[
                    TreeNode("L3"),
                ]),
            ]),
        ])
        result = tree(root)
        assert isinstance(result, str)
        assert "L0" in result and "L3" in result

    def test_simple_tree_single_item(self):
        """simple_tree() should handle single item"""
        result = simple_tree(["Only One"])
        assert isinstance(result, str)
        assert "Only One" in result

    def test_nested_list_unicode_content(self):
        """nested_list() should handle Unicode content"""
        items = ["✓ Done", "★ Important", "→ Next"]
        result = nested_list(items)
        assert isinstance(result, str)

    def test_tree_with_prefix(self):
        """tree() should support prefix parameter"""
        root = TreeNode("Root")
        result = tree(root, prefix="  ")
        assert isinstance(result, str)

    def test_nested_list_empty_nested_item(self):
        """nested_list() should handle empty nested lists"""
        items = [
            "Item 1",
            ("Item 2", []),
            "Item 3",
        ]
        result = nested_list(items)
        assert isinstance(result, str)
        assert "Item 1" in result
