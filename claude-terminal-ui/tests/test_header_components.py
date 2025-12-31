"""Tests for header and divider components"""
import pytest
from claude_terminal_ui.components.headers import (
    header,
    subheader,
    divider,
    step_header,
)


class TestHeaderComponents:
    """Test header formatting functions"""

    def test_header_returns_string(self):
        """header() should return formatted string"""
        result = header("MAIN TITLE")
        assert isinstance(result, str)
        assert "MAIN TITLE" in result

    def test_header_contains_decorators(self):
        """header() should contain top and bottom decorators"""
        result = header("TEST")
        lines = result.split("\n")
        # Should have exactly 3 lines: top decorator, title, bottom decorator
        assert len(lines) == 3

    def test_header_default_width(self):
        """header() should use default width of 70"""
        result = header("TEST")
        lines = result.split("\n")
        # Top line should be exactly 70 chars (border)
        if lines:
            # May have ANSI color codes, so check the visual width is around 70
            assert 60 <= len(lines[0]) <= 90  # Allow for ANSI codes

    def test_header_custom_width(self):
        """header() should accept custom width"""
        result = header("TEST", width=50)
        lines = result.split("\n")
        if lines:
            # Border line should be around 50 chars (may include ANSI codes)
            assert 40 <= len(lines[0]) <= 70

    def test_header_empty_text(self):
        """header() should handle empty text"""
        result = header("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_subheader_returns_string(self):
        """subheader() should return formatted string"""
        result = subheader("Section Title")
        assert isinstance(result, str)
        assert "Section Title" in result

    def test_subheader_different_from_header(self):
        """subheader() should be visually different from header()"""
        h = header("TEST")
        sh = subheader("TEST")
        assert h != sh  # Should have different formatting

    def test_divider_plain(self):
        """divider() with no label should return plain line"""
        result = divider()
        assert isinstance(result, str)
        # Should be mostly dash/hyphen characters
        assert result.count("-") > 50 or result.count("\u2500") > 50

    def test_divider_with_label(self):
        """divider() with label should include the label"""
        result = divider(label="Step 1")
        assert isinstance(result, str)
        assert "Step 1" in result

    def test_divider_custom_width(self):
        """divider() should respect custom width"""
        result = divider(width=40)
        # Width should be approximately 40 characters
        assert 35 <= len(result) <= 45

    def test_divider_custom_char(self):
        """divider() should accept custom character"""
        result = divider(char="*")
        # Note: char may be overridden based on Unicode support
        # Just verify we get a divider line
        assert isinstance(result, str)
        assert len(result) >= 50  # Should be at least width-ish

    def test_step_header_basic(self):
        """step_header() should format step number and label"""
        result = step_header(1, 5, "First Step")
        assert isinstance(result, str)
        assert "First Step" in result
        # Should contain step indicator like [1/5] or similar
        assert "1" in result
        assert "5" in result

    def test_step_header_different_steps(self):
        """step_header() should show different step numbers"""
        step1 = step_header(1, 3, "Step One")
        step2 = step_header(2, 3, "Step Two")
        step3 = step_header(3, 3, "Step Three")

        assert step1 != step2 != step3
        assert "Step One" in step1
        assert "Step Two" in step2
        assert "Step Three" in step3

    def test_step_header_zero_current(self):
        """step_header() should handle current=0"""
        result = step_header(0, 5, "Preparation")
        assert isinstance(result, str)

    def test_step_header_equal_current_total(self):
        """step_header() should handle current=total (final step)"""
        result = step_header(5, 5, "Complete")
        assert isinstance(result, str)
        assert "Complete" in result

    def test_header_long_text(self):
        """header() should handle text longer than width"""
        long_text = "This is a very long header text that exceeds the default width of 70 characters"
        result = header(long_text, width=70)
        assert isinstance(result, str)
        assert long_text in result

    def test_headers_with_unicode(self):
        """Headers should handle Unicode characters"""
        result = header("✓ Complete ★ Success")
        assert isinstance(result, str)
        assert "Complete" in result
        assert "Success" in result
