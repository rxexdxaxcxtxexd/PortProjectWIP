"""
Tests for spacing and layout constants

Tests cover:
- Standard width constants
- Padding and indentation values
- Progress bar widths
- Margin constants
- Constant immutability
"""

import pytest
from claude_terminal_ui.tokens.spacing import (
    DEFAULT_WIDTH,
    WIDE_WIDTH,
    NARROW_WIDTH,
    CELL_PADDING,
    INDENT_UNIT,
    LIST_INDENT,
    PROGRESS_BAR_WIDTH,
    PROGRESS_BAR_WIDTH_NARROW,
    TOP_MARGIN,
    BOTTOM_MARGIN,
    SECTION_SPACING,
)


class TestWidthConstants:
    """Test standard width constants"""

    def test_default_width_value(self):
        """DEFAULT_WIDTH should be 70"""
        assert DEFAULT_WIDTH == 70

    def test_wide_width_value(self):
        """WIDE_WIDTH should be 100"""
        assert WIDE_WIDTH == 100

    def test_narrow_width_value(self):
        """NARROW_WIDTH should be 60"""
        assert NARROW_WIDTH == 60

    def test_width_hierarchy(self):
        """Width constants should follow logical hierarchy"""
        assert NARROW_WIDTH < DEFAULT_WIDTH < WIDE_WIDTH

    def test_widths_are_integers(self):
        """All width constants should be integers"""
        assert isinstance(DEFAULT_WIDTH, int)
        assert isinstance(WIDE_WIDTH, int)
        assert isinstance(NARROW_WIDTH, int)

    def test_widths_positive(self):
        """All width constants should be positive"""
        assert DEFAULT_WIDTH > 0
        assert WIDE_WIDTH > 0
        assert NARROW_WIDTH > 0


class TestPaddingConstants:
    """Test padding and indentation constants"""

    def test_cell_padding_value(self):
        """CELL_PADDING should be 1"""
        assert CELL_PADDING == 1

    def test_indent_unit_value(self):
        """INDENT_UNIT should be 2 spaces"""
        assert INDENT_UNIT == 2

    def test_list_indent_value(self):
        """LIST_INDENT should be 2 spaces"""
        assert LIST_INDENT == 2

    def test_padding_are_integers(self):
        """All padding constants should be integers"""
        assert isinstance(CELL_PADDING, int)
        assert isinstance(INDENT_UNIT, int)
        assert isinstance(LIST_INDENT, int)

    def test_padding_non_negative(self):
        """All padding constants should be non-negative"""
        assert CELL_PADDING >= 0
        assert INDENT_UNIT >= 0
        assert LIST_INDENT >= 0


class TestProgressBarConstants:
    """Test progress bar width constants"""

    def test_progress_bar_width_value(self):
        """PROGRESS_BAR_WIDTH should be 50"""
        assert PROGRESS_BAR_WIDTH == 50

    def test_progress_bar_width_narrow_value(self):
        """PROGRESS_BAR_WIDTH_NARROW should be 30"""
        assert PROGRESS_BAR_WIDTH_NARROW == 30

    def test_progress_bar_hierarchy(self):
        """Progress bar widths should follow hierarchy"""
        assert PROGRESS_BAR_WIDTH_NARROW < PROGRESS_BAR_WIDTH

    def test_progress_bar_widths_are_integers(self):
        """Progress bar widths should be integers"""
        assert isinstance(PROGRESS_BAR_WIDTH, int)
        assert isinstance(PROGRESS_BAR_WIDTH_NARROW, int)

    def test_progress_bar_widths_positive(self):
        """Progress bar widths should be positive"""
        assert PROGRESS_BAR_WIDTH > 0
        assert PROGRESS_BAR_WIDTH_NARROW > 0


class TestMarginConstants:
    """Test margin and spacing constants"""

    def test_top_margin_value(self):
        """TOP_MARGIN should be 1 line"""
        assert TOP_MARGIN == 1

    def test_bottom_margin_value(self):
        """BOTTOM_MARGIN should be 1 line"""
        assert BOTTOM_MARGIN == 1

    def test_section_spacing_value(self):
        """SECTION_SPACING should be 1 line"""
        assert SECTION_SPACING == 1

    def test_margins_are_integers(self):
        """All margin constants should be integers"""
        assert isinstance(TOP_MARGIN, int)
        assert isinstance(BOTTOM_MARGIN, int)
        assert isinstance(SECTION_SPACING, int)

    def test_margins_non_negative(self):
        """All margin constants should be non-negative"""
        assert TOP_MARGIN >= 0
        assert BOTTOM_MARGIN >= 0
        assert SECTION_SPACING >= 0


class TestConstantUsability:
    """Test practical usability of constants"""

    def test_default_width_usable_for_text_wrapping(self):
        """DEFAULT_WIDTH should be reasonable for text wrapping"""
        # Should fit within most terminals (80 cols)
        assert DEFAULT_WIDTH <= 80
        # Should be wide enough for readable text
        assert DEFAULT_WIDTH >= 40

    def test_progress_bar_fits_in_default_width(self):
        """Progress bar should fit within DEFAULT_WIDTH"""
        # Add some margin for [brackets] and percentage
        assert PROGRESS_BAR_WIDTH + 10 < DEFAULT_WIDTH

    def test_indent_unit_practical(self):
        """INDENT_UNIT should be practical for nesting"""
        # Multiple levels shouldn't take up too much space
        max_nesting = 5
        assert INDENT_UNIT * max_nesting < DEFAULT_WIDTH // 2

    def test_cell_padding_practical(self):
        """CELL_PADDING should provide minimal spacing"""
        # Should be small but visible
        assert 0 < CELL_PADDING <= 3


class TestConstantRelationships:
    """Test relationships between constants"""

    def test_wide_width_fits_audit_reports(self):
        """WIDE_WIDTH should accommodate wide tables"""
        # From analysis: audit reports use 100 width
        assert WIDE_WIDTH == 100

    def test_narrow_width_for_compact_display(self):
        """NARROW_WIDTH should be compact but readable"""
        assert NARROW_WIDTH >= 50  # Minimum for readability
        assert NARROW_WIDTH < DEFAULT_WIDTH

    def test_progress_bar_proportional_to_width(self):
        """Progress bar should be roughly proportional to default width"""
        # Should be about 2/3 of default width
        assert 0.5 < (PROGRESS_BAR_WIDTH / DEFAULT_WIDTH) < 0.8


class TestConstantDocumentation:
    """Test that constants have clear purposes"""

    def test_all_constants_defined(self):
        """All documented constants should be defined"""
        # Standard widths
        assert DEFAULT_WIDTH is not None
        assert WIDE_WIDTH is not None
        assert NARROW_WIDTH is not None

        # Padding
        assert CELL_PADDING is not None
        assert INDENT_UNIT is not None
        assert LIST_INDENT is not None

        # Progress bar
        assert PROGRESS_BAR_WIDTH is not None
        assert PROGRESS_BAR_WIDTH_NARROW is not None

        # Margins
        assert TOP_MARGIN is not None
        assert BOTTOM_MARGIN is not None
        assert SECTION_SPACING is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_zero_indentation_works(self):
        """0 * INDENT_UNIT should work for no indentation"""
        result = 0 * INDENT_UNIT
        assert result == 0

    def test_multiple_indentation_levels(self):
        """Multiple indentation levels should compound properly"""
        level_2 = 2 * INDENT_UNIT
        level_3 = 3 * INDENT_UNIT
        assert level_3 == level_2 + INDENT_UNIT

    def test_progress_bar_minimum_width(self):
        """Even narrow progress bar should be usable"""
        # Should have at least 20 chars for visibility
        assert PROGRESS_BAR_WIDTH_NARROW >= 20

    def test_constants_immutable(self):
        """Constants should be simple immutable types"""
        # All should be integers (immutable)
        constants = [
            DEFAULT_WIDTH,
            WIDE_WIDTH,
            NARROW_WIDTH,
            CELL_PADDING,
            INDENT_UNIT,
            LIST_INDENT,
            PROGRESS_BAR_WIDTH,
            PROGRESS_BAR_WIDTH_NARROW,
            TOP_MARGIN,
            BOTTOM_MARGIN,
            SECTION_SPACING,
        ]
        assert all(isinstance(c, int) for c in constants)


class TestPracticalExamples:
    """Test practical usage scenarios"""

    def test_centered_text_calculation(self):
        """Test centering text within DEFAULT_WIDTH"""
        text = "Test Header"
        padding = (DEFAULT_WIDTH - len(text)) // 2
        assert padding >= 0
        assert padding + len(text) <= DEFAULT_WIDTH

    def test_indented_list_formatting(self):
        """Test nested list indentation"""
        level_1_indent = LIST_INDENT
        level_2_indent = LIST_INDENT * 2
        level_3_indent = LIST_INDENT * 3

        # All levels should fit within default width
        max_indent = level_3_indent
        min_text_space = 30  # Minimum space for text
        assert max_indent + min_text_space < DEFAULT_WIDTH

    def test_table_with_cell_padding(self):
        """Test table cell width calculation with padding"""
        num_columns = 3
        total_padding = num_columns * CELL_PADDING * 2  # Left and right
        content_width = DEFAULT_WIDTH - total_padding
        assert content_width > 0

    def test_progress_bar_with_label(self):
        """Test progress bar with percentage label fits"""
        bar_width = PROGRESS_BAR_WIDTH
        label = " 100%"
        brackets = "[]"
        total = bar_width + len(label) + len(brackets)
        assert total < DEFAULT_WIDTH

    def test_section_with_margins(self):
        """Test section spacing calculation"""
        num_sections = 5
        total_margin_lines = (num_sections - 1) * SECTION_SPACING
        total_margin_lines += TOP_MARGIN + BOTTOM_MARGIN
        # Should be reasonable
        assert total_margin_lines < 20
