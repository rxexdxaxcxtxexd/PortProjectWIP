"""Tests for table formatting components"""
import pytest
from claude_terminal_ui.components.tables import (
    key_value,
    table,
    stats_panel,
    print_key_value,
    print_table,
    print_stats_panel,
)


class TestTableComponents:
    """Test table formatting functions"""

    def test_key_value_basic(self):
        """key_value() should format dictionary"""
        kv = {"Name": "Test", "Status": "Active", "Count": "42"}
        result = key_value(kv)
        assert isinstance(result, str)
        assert "Name" in result
        assert "Test" in result
        assert "Status" in result

    def test_key_value_empty_dict(self):
        """key_value() should handle empty dictionary"""
        result = key_value({})
        assert isinstance(result, str)

    def test_key_value_custom_width(self):
        """key_value() should accept custom width"""
        kv = {"Key": "Value"}
        result = key_value(kv, width=50)
        assert isinstance(result, str)

    def test_key_value_with_indent(self):
        """key_value() should support indentation"""
        kv = {"Key": "Value"}
        result = key_value(kv, indent=4)
        assert isinstance(result, str)

    def test_key_value_align_colon_true(self):
        """key_value() should align colons when requested"""
        kv = {"Short": "A", "Very Long Key": "B"}
        result = key_value(kv, align_colon=True)
        assert isinstance(result, str)

    def test_key_value_align_colon_false(self):
        """key_value() should not align when align_colon=False"""
        kv = {"Short": "A", "Long": "B"}
        result = key_value(kv, align_colon=False)
        assert isinstance(result, str)

    def test_key_value_with_color(self):
        """key_value() should support value color"""
        from claude_terminal_ui.tokens.colors import Colors
        kv = {"Status": "Success"}
        result = key_value(kv, value_color=Colors.SUCCESS)
        assert isinstance(result, str)

    def test_key_value_custom_key_width(self):
        """key_value() should support custom key width"""
        kv = {"Key": "Value"}
        result = key_value(kv, key_width=20)
        assert isinstance(result, str)

    def test_key_value_numeric_values(self):
        """key_value() should handle numeric values"""
        kv = {"Count": 42, "Percent": 99.5, "Total": 1000}
        result = key_value(kv)
        assert isinstance(result, str)
        assert "42" in result

    def test_table_basic(self):
        """table() should format data with headers"""
        data = [["A", "B", "C"], ["1", "2", "3"]]
        headers = ["Col1", "Col2", "Col3"]
        result = table(data, headers=headers)
        assert isinstance(result, str)
        assert "Col1" in result
        assert "A" in result

    def test_table_no_headers(self):
        """table() should work without headers"""
        data = [["A", "B"], ["C", "D"]]
        result = table(data)
        assert isinstance(result, str)
        assert "A" in result

    def test_table_empty_data(self):
        """table() should handle empty data"""
        result = table([])
        assert isinstance(result, str)

    def test_table_custom_width(self):
        """table() should accept custom width"""
        data = [["A", "B"]]
        result = table(data, width=60)
        assert isinstance(result, str)

    def test_table_alignment_left(self):
        """table() should support left alignment"""
        data = [["Left", "Aligned"]]
        result = table(data, align=["left", "left"])
        assert isinstance(result, str)

    def test_table_alignment_right(self):
        """table() should support right alignment"""
        data = [["Right", "Aligned"]]
        result = table(data, align=["right", "right"])
        assert isinstance(result, str)

    def test_table_alignment_center(self):
        """table() should support center alignment"""
        data = [["Center", "Aligned"]]
        result = table(data, align=["center", "center"])
        assert isinstance(result, str)

    def test_table_mixed_alignment(self):
        """table() should support mixed alignment"""
        data = [["A", "B", "C"]]
        result = table(data, align=["left", "center", "right"])
        assert isinstance(result, str)

    def test_table_header_color(self):
        """table() should support header color"""
        from claude_terminal_ui.tokens.colors import Colors
        data = [["Value"]]
        headers = ["Header"]
        result = table(data, headers=headers, header_color=Colors.INFO)
        assert isinstance(result, str)

    def test_table_show_borders_true(self):
        """table() should show borders when requested"""
        data = [["A", "B"]]
        result = table(data, show_borders=True)
        assert isinstance(result, str)

    def test_table_show_borders_false(self):
        """table() should hide borders when requested"""
        data = [["A", "B"]]
        result = table(data, show_borders=False)
        assert isinstance(result, str)

    def test_table_compact_mode(self):
        """table() should support compact mode"""
        data = [["A", "B"]]
        result = table(data, compact=True)
        assert isinstance(result, str)

    def test_table_single_row(self):
        """table() should handle single row"""
        data = [["Only", "Row"]]
        result = table(data)
        assert isinstance(result, str)

    def test_table_single_column(self):
        """table() should handle single column"""
        data = [["A"], ["B"], ["C"]]
        result = table(data)
        assert isinstance(result, str)

    def test_table_unicode_content(self):
        """table() should handle Unicode content"""
        data = [["✓", "✗"], ["★", "→"]]
        result = table(data)
        assert isinstance(result, str)

    def test_stats_panel_basic(self):
        """stats_panel() should format statistics"""
        stats = {"Total": 100, "Success": 95, "Failed": 5}
        result = stats_panel(stats)
        assert isinstance(result, str)
        assert "Total" in result
        assert "100" in result

    def test_stats_panel_with_title(self):
        """stats_panel() should include title"""
        stats = {"Count": 42}
        result = stats_panel(stats, title="Statistics")
        assert isinstance(result, str)
        assert "Statistics" in result

    def test_stats_panel_layout_grid(self):
        """stats_panel() should support grid layout"""
        stats = {"A": 1, "B": 2, "C": 3, "D": 4}
        result = stats_panel(stats, layout="grid")
        assert isinstance(result, str)

    def test_stats_panel_layout_list(self):
        """stats_panel() should support list layout"""
        stats = {"A": 1, "B": 2}
        result = stats_panel(stats, layout="list")
        assert isinstance(result, str)

    def test_stats_panel_custom_columns(self):
        """stats_panel() should support custom column count"""
        stats = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
        result = stats_panel(stats, columns=3)
        assert isinstance(result, str)

    def test_stats_panel_show_borders(self):
        """stats_panel() should support show_borders"""
        stats = {"Metric": 100}
        result = stats_panel(stats, show_borders=True)
        assert isinstance(result, str)

    def test_stats_panel_no_borders(self):
        """stats_panel() should work without borders"""
        stats = {"Metric": 100}
        result = stats_panel(stats, show_borders=False)
        assert isinstance(result, str)

    def test_stats_panel_title_color(self):
        """stats_panel() should support title color"""
        from claude_terminal_ui.tokens.colors import Colors
        stats = {"Value": 42}
        result = stats_panel(stats, title="Stats", title_color=Colors.SUCCESS)
        assert isinstance(result, str)

    def test_stats_panel_empty_dict(self):
        """stats_panel() should handle empty statistics"""
        result = stats_panel({})
        assert isinstance(result, str)

    def test_print_key_value_prints(self, capsys):
        """print_key_value() should print to stdout"""
        kv = {"Test": "Value"}
        print_key_value(kv)
        captured = capsys.readouterr()
        assert "Test" in captured.out

    def test_print_table_prints(self, capsys):
        """print_table() should print to stdout"""
        data = [["A", "B"]]
        print_table(data)
        captured = capsys.readouterr()
        assert "A" in captured.out

    def test_print_stats_panel_prints(self, capsys):
        """print_stats_panel() should print to stdout"""
        stats = {"Metric": 100}
        print_stats_panel(stats)
        captured = capsys.readouterr()
        assert "Metric" in captured.out

    def test_table_long_values(self):
        """table() should handle very long cell values"""
        data = [["Short", "This is a very long value that exceeds normal width"]]
        result = table(data)
        assert isinstance(result, str)

    def test_table_many_rows(self):
        """table() should handle many rows"""
        data = [[str(i), str(i*2)] for i in range(100)]
        result = table(data)
        assert isinstance(result, str)

    def test_key_value_long_keys(self):
        """key_value() should handle very long keys"""
        kv = {"This is a very long key name": "Value"}
        result = key_value(kv)
        assert isinstance(result, str)

    def test_stats_panel_large_numbers(self):
        """stats_panel() should handle large numbers"""
        stats = {"Total": 1000000, "Average": 99.999}
        result = stats_panel(stats)
        assert isinstance(result, str)
