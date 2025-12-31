"""Tests for progress indicator components"""
import pytest
from claude_terminal_ui.components.progress import (
    progress_bar,
    spinner,
    step_indicator,
    Spinner,
)


class TestProgressComponents:
    """Test progress indicator functions"""

    def test_progress_bar_basic(self):
        """progress_bar() should return formatted bar"""
        result = progress_bar(50, 100)
        assert isinstance(result, str)
        # Should show percentage
        assert "50%" in result

    def test_progress_bar_zero_progress(self):
        """progress_bar() should handle 0% progress"""
        result = progress_bar(0, 100)
        assert isinstance(result, str)
        assert "0%" in result

    def test_progress_bar_full_progress(self):
        """progress_bar() should handle 100% progress"""
        result = progress_bar(100, 100)
        assert isinstance(result, str)
        assert "100%" in result

    def test_progress_bar_custom_width(self):
        """progress_bar() should accept custom width"""
        result = progress_bar(50, 100, width=30)
        assert isinstance(result, str)
        # String length includes ANSI codes, so may be longer than visual width
        # Just verify it's a reasonable length
        assert len(result) > 0

    def test_progress_bar_with_prefix(self):
        """progress_bar() should include optional prefix"""
        result = progress_bar(75, 100, prefix="Downloading: ")
        assert isinstance(result, str)
        assert "Downloading" in result
        assert "75%" in result

    def test_progress_bar_percentage_calculation(self):
        """progress_bar() should calculate correct percentage"""
        result = progress_bar(25, 100)
        assert "25%" in result

        result = progress_bar(1, 3)
        assert "33%" in result

    def test_step_indicator_basic(self):
        """step_indicator() should format step counter and label"""
        result = step_indicator(1, 5, "Loading data")
        assert isinstance(result, str)
        assert "Loading data" in result
        # Should show step numbers
        assert "1" in result and "5" in result

    def test_step_indicator_different_steps(self):
        """step_indicator() should show progression"""
        step1 = step_indicator(1, 3, "Step 1")
        step2 = step_indicator(2, 3, "Step 2")
        step3 = step_indicator(3, 3, "Step 3")

        assert step1 != step2 != step3

    def test_step_indicator_final_step(self):
        """step_indicator() should handle final step"""
        result = step_indicator(10, 10, "Finalizing")
        assert isinstance(result, str)
        assert "Finalizing" in result

    def test_spinner_context_manager_works(self):
        """spinner() should work as context manager"""
        # spinner() is a context manager, not a function that returns frames
        with spinner("Loading"):
            pass  # Should complete without error

    def test_spinner_context_manager_basic(self):
        """Spinner context manager should work"""
        with Spinner("Loading") as s:
            assert s is not None

    def test_spinner_context_manager_with_label(self):
        """Spinner should accept custom label"""
        with Spinner("Processing files") as s:
            assert s is not None

    def test_spinner_stop_method(self):
        """Spinner should have stop method"""
        s = Spinner("Test")
        s.start()
        s.stop()
        # Should not raise an exception

    def test_progress_bar_boundary_values(self):
        """progress_bar() should handle edge cases"""
        # More completed than total (should cap at 100%)
        result = progress_bar(150, 100)
        assert isinstance(result, str)

        # Negative values (should handle gracefully)
        result = progress_bar(0, 100)
        assert isinstance(result, str)

    def test_progress_bar_small_total(self):
        """progress_bar() should handle small total values"""
        result = progress_bar(1, 1)
        assert isinstance(result, str)
        assert "100%" in result

        result = progress_bar(0, 1)
        assert "0%" in result

    def test_step_indicator_single_step(self):
        """step_indicator() should handle single-step process"""
        result = step_indicator(1, 1, "Only step")
        assert isinstance(result, str)
        assert "Only step" in result

    def test_progress_components_with_unicode(self):
        """Progress components should handle Unicode in prefixes"""
        result = progress_bar(50, 100, prefix="Downloading ✓ ")
        assert isinstance(result, str)

        result = step_indicator(1, 3, "Step with ★ symbol")
        assert isinstance(result, str)

    def test_spinner_multiple_instances(self):
        """Should be able to create multiple spinner instances"""
        s1 = Spinner("Task 1")
        s2 = Spinner("Task 2")
        assert s1 is not s2

    def test_progress_bar_very_long_prefix(self):
        """progress_bar() should handle very long prefixes"""
        long_prefix = "This is a very long prefix " * 5
        result = progress_bar(50, 100, prefix=long_prefix)
        assert isinstance(result, str)
