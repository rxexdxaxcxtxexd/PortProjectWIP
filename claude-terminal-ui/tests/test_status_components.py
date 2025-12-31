"""Tests for status message components"""
import pytest
from claude_terminal_ui.components.status import (
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


class TestStatusMessages:
    """Test status message formatting functions"""

    def test_success_returns_string(self):
        """success() should return formatted string"""
        result = success("Operation completed")
        assert isinstance(result, str)
        assert "Operation completed" in result

    def test_success_contains_indicator(self):
        """success() should contain success indicator"""
        result = success("Test message")
        # Should contain either [OK] or ✓ depending on Unicode support
        assert "[OK]" in result or "\u2714" in result

    def test_error_returns_string(self):
        """error() should return formatted string"""
        result = error("Operation failed")
        assert isinstance(result, str)
        assert "Operation failed" in result

    def test_error_contains_indicator(self):
        """error() should contain error indicator"""
        result = error("Test message")
        assert "[ERROR]" in result or "[X]" in result or "\u2718" in result

    def test_warning_returns_string(self):
        """warning() should return formatted string"""
        result = warning("Disk space low")
        assert isinstance(result, str)
        assert "Disk space low" in result

    def test_warning_contains_indicator(self):
        """warning() should contain warning indicator"""
        result = warning("Test message")
        assert "[WARNING]" in result or "[!]" in result or "\u26a0" in result

    def test_info_returns_string(self):
        """info() should return formatted string"""
        result = info("Processing files")
        assert isinstance(result, str)
        assert "Processing files" in result

    def test_info_contains_indicator(self):
        """info() should contain info indicator"""
        result = info("Test message")
        assert "[INFO]" in result or "[i]" in result or "\u2139" in result

    def test_debug_returns_string(self):
        """debug() should return formatted string"""
        result = debug("Cache hit: 85%")
        assert isinstance(result, str)
        assert "Cache hit: 85%" in result

    def test_debug_contains_indicator(self):
        """debug() should contain debug indicator"""
        result = debug("Test message")
        assert "[DEBUG]" in result or "[D]" in result or "\u2699" in result

    def test_print_success_prints(self, capsys):
        """print_success() should print to stdout"""
        print_success("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_print_error_prints(self, capsys):
        """print_error() should print to stdout"""
        print_error("Test error")
        captured = capsys.readouterr()
        assert "Test error" in captured.out

    def test_print_warning_prints(self, capsys):
        """print_warning() should print to stdout"""
        print_warning("Test warning")
        captured = capsys.readouterr()
        assert "Test warning" in captured.out

    def test_print_info_prints(self, capsys):
        """print_info() should print to stdout"""
        print_info("Test info")
        captured = capsys.readouterr()
        assert "Test info" in captured.out

    def test_print_debug_prints(self, capsys):
        """print_debug() should print to stdout"""
        print_debug("Test debug")
        captured = capsys.readouterr()
        assert "Test debug" in captured.out

    def test_empty_message(self):
        """Status functions should handle empty messages"""
        result = success("")
        assert isinstance(result, str)
        # Should still have indicator even with empty message
        assert len(result) > 0

    def test_multiline_message(self):
        """Status functions should handle multiline messages"""
        message = "Line 1\\nLine 2\\nLine 3"
        result = success(message)
        assert isinstance(result, str)
        assert message in result

    def test_unicode_in_message(self):
        """Status functions should handle Unicode in messages"""
        message = "Files: ✓ tests ✗ build"
        result = info(message)
        assert isinstance(result, str)
        assert "tests" in result
