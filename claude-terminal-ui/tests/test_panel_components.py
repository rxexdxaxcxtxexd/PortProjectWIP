"""Tests for panel and box components"""
import pytest
from claude_terminal_ui.components.panels import (
    panel,
    box,
    info_panel,
    titled_box,
    compact_panel,
)


class TestPanelComponents:
    """Test panel and box functions"""

    def test_panel_basic(self):
        """panel() should create bordered content"""
        result = panel("Test content")
        assert isinstance(result, str)
        assert "Test content" in result

    def test_panel_with_title(self):
        """panel() should include title"""
        result = panel("Content", title="Header")
        assert isinstance(result, str)
        assert "Header" in result
        assert "Content" in result

    def test_panel_custom_width(self):
        """panel() should accept custom width"""
        result = panel("Text", width=40)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_panel_multiline_content(self):
        """panel() should handle multiline content"""
        content = "Line 1\\nLine 2\\nLine 3"
        result = panel(content)
        assert isinstance(result, str)

    def test_panel_with_color(self):
        """panel() should support color"""
        from claude_terminal_ui.tokens.colors import Colors
        result = panel("Colored", color=Colors.INFO)
        assert isinstance(result, str)
        assert "Colored" in result

    def test_panel_with_padding(self):
        """panel() should support padding"""
        result = panel("Text", padding=2)
        assert isinstance(result, str)

    def test_panel_alignment_left(self):
        """panel() should support left alignment"""
        result = panel("Left", align="left")
        assert isinstance(result, str)

    def test_panel_alignment_center(self):
        """panel() should support center alignment"""
        result = panel("Center", align="center")
        assert isinstance(result, str)

    def test_panel_alignment_right(self):
        """panel() should support right alignment"""
        result = panel("Right", align="right")
        assert isinstance(result, str)

    def test_box_basic(self):
        """box() should create simple box"""
        result = box("Boxed text")
        assert isinstance(result, str)
        assert "Boxed text" in result

    def test_box_custom_width(self):
        """box() should accept custom width"""
        result = box("Text", width=50)
        assert isinstance(result, str)

    def test_box_with_color(self):
        """box() should support color"""
        from claude_terminal_ui.tokens.colors import Colors
        result = box("Colored", color=Colors.WARNING)
        assert isinstance(result, str)

    def test_info_panel_basic(self):
        """info_panel() should create info panel"""
        result = info_panel("Information message")
        assert isinstance(result, str)
        assert "Information message" in result

    def test_info_panel_with_title(self):
        """info_panel() should support title"""
        result = info_panel("Message", title="Note")
        assert isinstance(result, str)
        assert "Note" in result

    def test_info_panel_type_info(self):
        """info_panel() should support info type"""
        result = info_panel("Info", panel_type="info")
        assert isinstance(result, str)

    def test_info_panel_type_success(self):
        """info_panel() should support success type"""
        result = info_panel("Success", panel_type="success")
        assert isinstance(result, str)

    def test_info_panel_type_warning(self):
        """info_panel() should support warning type"""
        result = info_panel("Warning", panel_type="warning")
        assert isinstance(result, str)

    def test_info_panel_type_error(self):
        """info_panel() should support error type"""
        result = info_panel("Error", panel_type="error")
        assert isinstance(result, str)

    def test_info_panel_type_debug(self):
        """info_panel() should support debug type"""
        result = info_panel("Debug", panel_type="debug")
        assert isinstance(result, str)

    def test_titled_box_basic(self):
        """titled_box() should create box with title and items"""
        items = ["Item 1", "Item 2", "Item 3"]
        result = titled_box(items, title="List")
        assert isinstance(result, str)
        assert "List" in result
        assert "Item 1" in result

    def test_titled_box_empty_items(self):
        """titled_box() should handle empty item list"""
        result = titled_box([], title="Empty")
        assert isinstance(result, str)
        assert "Empty" in result

    def test_titled_box_single_item(self):
        """titled_box() should handle single item"""
        result = titled_box(["Only one"], title="Single")
        assert isinstance(result, str)
        assert "Only one" in result

    def test_titled_box_custom_bullet(self):
        """titled_box() should support custom bullet"""
        items = ["A", "B"]
        result = titled_box(items, title="Custom", bullet="-")
        assert isinstance(result, str)

    def test_titled_box_with_color(self):
        """titled_box() should support color"""
        from claude_terminal_ui.tokens.colors import Colors
        items = ["One"]
        result = titled_box(items, title="Colored", color=Colors.SUCCESS)
        assert isinstance(result, str)

    def test_compact_panel_basic(self):
        """compact_panel() should create panel with key-value pairs"""
        kv = {"Name": "Test", "Status": "Active"}
        result = compact_panel(kv)
        assert isinstance(result, str)
        assert "Name" in result
        assert "Test" in result

    def test_compact_panel_with_title(self):
        """compact_panel() should support title"""
        kv = {"Key": "Value"}
        result = compact_panel(kv, title="Info")
        assert isinstance(result, str)
        assert "Info" in result

    def test_compact_panel_empty_dict(self):
        """compact_panel() should handle empty dictionary"""
        result = compact_panel({})
        assert isinstance(result, str)

    def test_compact_panel_many_items(self):
        """compact_panel() should handle many key-value pairs"""
        kv = {f"Key{i}": f"Value{i}" for i in range(10)}
        result = compact_panel(kv)
        assert isinstance(result, str)

    def test_compact_panel_with_color(self):
        """compact_panel() should support color"""
        from claude_terminal_ui.tokens.colors import Colors
        kv = {"Test": "Value"}
        result = compact_panel(kv, color=Colors.INFO)
        assert isinstance(result, str)

    def test_panel_empty_content(self):
        """panel() should handle empty content"""
        result = panel("")
        assert isinstance(result, str)

    def test_box_multiline(self):
        """box() should handle multiline content"""
        content = "Line 1\\nLine 2\\nLine 3"
        result = box(content)
        assert isinstance(result, str)

    def test_titled_box_unicode_items(self):
        """titled_box() should handle Unicode in items"""
        items = ["✓ Complete", "★ Important"]
        result = titled_box(items, title="Tasks")
        assert isinstance(result, str)

    def test_compact_panel_unicode_values(self):
        """compact_panel() should handle Unicode values"""
        kv = {"Status": "✓ Active", "Priority": "★ High"}
        result = compact_panel(kv)
        assert isinstance(result, str)

    def test_info_panel_custom_width(self):
        """info_panel() should support custom width"""
        result = info_panel("Message", width=60)
        assert isinstance(result, str)

    def test_panel_long_content(self):
        """panel() should handle very long content"""
        long_content = "Word " * 100
        result = panel(long_content)
        assert isinstance(result, str)
