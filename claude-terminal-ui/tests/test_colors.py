"""
Tests for color token system

Tests cover:
- Color class with ANSI code generation
- Color.code() with different ColorSupport levels
- Colors semantic color definitions
- BgColors background colors
- Styles text formatting
- colorize() helper function
- Graceful degradation
"""

import pytest
from unittest.mock import patch
from claude_terminal_ui.core.capabilities import ColorSupport, reset_capabilities
from claude_terminal_ui.tokens.colors import (
    Color,
    Colors,
    BgColors,
    Styles,
    RESET,
    colorize,
)


class TestColorClass:
    """Test Color dataclass and code generation"""

    def test_color_attributes(self):
        """Color should have all required attributes"""
        color = Color("test", "\033[31m", 196, (231, 76, 60))
        assert color.name == "test"
        assert color.ansi_16 == "\033[31m"
        assert color.ansi_256 == 196
        assert color.rgb == (231, 76, 60)

    def test_code_with_no_color_support(self):
        """ColorSupport.NONE should return empty string"""
        color = Color("test", "\033[31m", 196, (231, 76, 60))
        assert color.code(ColorSupport.NONE) == ""

    def test_code_with_basic_color_support(self):
        """ColorSupport.BASIC should return ANSI 16 code"""
        color = Color("test", "\033[31m", 196, (231, 76, 60))
        assert color.code(ColorSupport.BASIC) == "\033[31m"

    def test_code_with_extended_color_support(self):
        """ColorSupport.EXTENDED should return 256-color code"""
        color = Color("test", "\033[31m", 196, (231, 76, 60))
        result = color.code(ColorSupport.EXTENDED)
        assert result == "\033[38;5;196m"

    def test_code_with_truecolor_support(self):
        """ColorSupport.TRUECOLOR should return RGB code"""
        color = Color("test", "\033[31m", 196, (231, 76, 60))
        result = color.code(ColorSupport.TRUECOLOR)
        assert result == "\033[38;2;231;76;60m"

    def test_code_without_explicit_support(self, mock_full_capabilities):
        """code() without args should auto-detect from get_capabilities()"""
        color = Colors.SUCCESS
        result = color.code()
        # Should use truecolor (from mock_full_capabilities)
        assert result == "\033[38;2;46;204;113m"

    def test_code_without_explicit_support_no_color(self, mock_minimal_capabilities):
        """code() should respect NO_COLOR from capabilities"""
        color = Colors.SUCCESS
        result = color.code()
        assert result == ""


class TestColorsSemanticDefinitions:
    """Test predefined semantic color definitions"""

    def test_success_color_exists(self):
        """Colors.SUCCESS should be defined"""
        assert Colors.SUCCESS.name == "success"
        assert isinstance(Colors.SUCCESS.rgb, tuple)
        assert len(Colors.SUCCESS.rgb) == 3

    def test_error_color_exists(self):
        """Colors.ERROR should be defined"""
        assert Colors.ERROR.name == "error"

    def test_warning_color_exists(self):
        """Colors.WARNING should be defined"""
        assert Colors.WARNING.name == "warning"

    def test_info_color_exists(self):
        """Colors.INFO should be defined"""
        assert Colors.INFO.name == "info"

    def test_debug_color_exists(self):
        """Colors.DEBUG should be defined"""
        assert Colors.DEBUG.name == "debug"

    def test_primary_color_exists(self):
        """Colors.PRIMARY should be defined"""
        assert Colors.PRIMARY.name == "primary"

    def test_secondary_color_exists(self):
        """Colors.SECONDARY should be defined"""
        assert Colors.SECONDARY.name == "secondary"

    def test_muted_color_exists(self):
        """Colors.MUTED should be defined"""
        assert Colors.MUTED.name == "muted"

    def test_accent_color_exists(self):
        """Colors.ACCENT should be defined"""
        assert Colors.ACCENT.name == "accent"

    def test_highlight_color_exists(self):
        """Colors.HIGHLIGHT should be defined"""
        assert Colors.HIGHLIGHT.name == "highlight"

    def test_link_color_exists(self):
        """Colors.LINK should be defined"""
        assert Colors.LINK.name == "link"

    def test_add_color_exists(self):
        """Colors.ADD should be defined (git/diff)"""
        assert Colors.ADD.name == "add"

    def test_remove_color_exists(self):
        """Colors.REMOVE should be defined (git/diff)"""
        assert Colors.REMOVE.name == "remove"

    def test_change_color_exists(self):
        """Colors.CHANGE should be defined (git/diff)"""
        assert Colors.CHANGE.name == "change"

    def test_all_colors_have_valid_rgb(self):
        """All color RGB values should be valid (0-255)"""
        for attr_name in dir(Colors):
            if attr_name.isupper():
                color = getattr(Colors, attr_name)
                if isinstance(color, Color):
                    r, g, b = color.rgb
                    assert 0 <= r <= 255, f"{attr_name} red out of range"
                    assert 0 <= g <= 255, f"{attr_name} green out of range"
                    assert 0 <= b <= 255, f"{attr_name} blue out of range"

    def test_all_colors_have_valid_ansi256(self):
        """All color ANSI 256 values should be valid (0-255)"""
        for attr_name in dir(Colors):
            if attr_name.isupper():
                color = getattr(Colors, attr_name)
                if isinstance(color, Color):
                    assert 0 <= color.ansi_256 <= 255, f"{attr_name} ANSI 256 out of range"


class TestBgColors:
    """Test background color definitions"""

    def test_bg_success_exists(self):
        """BgColors.SUCCESS should be defined"""
        assert BgColors.SUCCESS.name == "bg_success"

    def test_bg_error_exists(self):
        """BgColors.ERROR should be defined"""
        assert BgColors.ERROR.name == "bg_error"

    def test_bg_warning_exists(self):
        """BgColors.WARNING should be defined"""
        assert BgColors.WARNING.name == "bg_warning"

    def test_bg_info_exists(self):
        """BgColors.INFO should be defined"""
        assert BgColors.INFO.name == "bg_info"

    def test_bg_colors_use_background_codes(self):
        """Background colors should use 4X ANSI codes"""
        # Basic ANSI background codes are 4X (40-47)
        assert BgColors.SUCCESS.ansi_16.startswith("\033[4")
        assert BgColors.ERROR.ansi_16.startswith("\033[4")


class TestStyles:
    """Test text style codes"""

    def test_bold_style(self):
        """BOLD style should be defined"""
        assert Styles.BOLD == "\033[1m"

    def test_dim_style(self):
        """DIM style should be defined"""
        assert Styles.DIM == "\033[2m"

    def test_italic_style(self):
        """ITALIC style should be defined"""
        assert Styles.ITALIC == "\033[3m"

    def test_underline_style(self):
        """UNDERLINE style should be defined"""
        assert Styles.UNDERLINE == "\033[4m"

    def test_blink_style(self):
        """BLINK style should be defined"""
        assert Styles.BLINK == "\033[5m"

    def test_reverse_style(self):
        """REVERSE style should be defined"""
        assert Styles.REVERSE == "\033[7m"

    def test_strikethrough_style(self):
        """STRIKETHROUGH style should be defined"""
        assert Styles.STRIKETHROUGH == "\033[9m"


class TestResetCode:
    """Test RESET escape code"""

    def test_reset_code_defined(self):
        """RESET should be defined"""
        assert RESET == "\033[0m"


class TestColorizeFunction:
    """Test colorize() helper function"""

    def test_colorize_with_color_support(self, mock_full_capabilities):
        """colorize() should wrap text with color codes"""
        result = colorize("test", Colors.SUCCESS)
        assert result.startswith("\033[38;2;46;204;113m")  # Truecolor
        assert result.endswith("\033[0m")
        assert "test" in result

    def test_colorize_with_bold(self, mock_full_capabilities):
        """colorize() with bold=True should add BOLD style"""
        result = colorize("test", Colors.SUCCESS, bold=True)
        assert Styles.BOLD in result
        assert "test" in result
        assert result.endswith(RESET)

    def test_colorize_no_color_support(self, mock_minimal_capabilities):
        """colorize() with NO_COLOR should return plain text"""
        result = colorize("test", Colors.SUCCESS)
        assert result == "test"

    def test_colorize_no_bold_without_color(self, mock_minimal_capabilities):
        """colorize() with NO_COLOR should ignore bold parameter"""
        result = colorize("test", Colors.SUCCESS, bold=True)
        assert result == "test"

    def test_colorize_preserves_text(self, mock_full_capabilities):
        """colorize() should not modify the actual text content"""
        text = "Hello, World!"
        result = colorize(text, Colors.INFO)
        # Remove ANSI codes to check text preservation
        clean = result.replace(Colors.INFO.code(), "").replace(RESET, "")
        assert clean == text


class TestColorDegradation:
    """Test graceful color degradation across support levels"""

    def test_success_color_degradation_none(self):
        """SUCCESS color should degrade to empty string with NO_COLOR"""
        assert Colors.SUCCESS.code(ColorSupport.NONE) == ""

    def test_success_color_degradation_basic(self):
        """SUCCESS color should use ANSI 16 with BASIC support"""
        assert Colors.SUCCESS.code(ColorSupport.BASIC) == "\033[32m"

    def test_success_color_degradation_256(self):
        """SUCCESS color should use 256-color with EXTENDED support"""
        result = Colors.SUCCESS.code(ColorSupport.EXTENDED)
        assert result == "\033[38;5;34m"

    def test_success_color_degradation_truecolor(self):
        """SUCCESS color should use RGB with TRUECOLOR support"""
        result = Colors.SUCCESS.code(ColorSupport.TRUECOLOR)
        assert result == "\033[38;2;46;204;113m"


class TestColorIntegrationWithCapabilities:
    """Test color system integration with capability detection"""

    def test_auto_detect_full_capabilities(self, mock_full_capabilities):
        """Should auto-detect truecolor from capabilities"""
        result = colorize("test", Colors.ERROR)
        # Should use truecolor
        assert "\033[38;2;" in result

    def test_auto_detect_basic_capabilities(self, mock_basic_color):
        """Should auto-detect basic color from capabilities"""
        result = colorize("test", Colors.ERROR)
        # Should use basic ANSI
        assert result.startswith("\033[1m\033[31m") or result.startswith("\033[31m")

    def test_auto_detect_no_color(self, mock_minimal_capabilities):
        """Should auto-detect NO_COLOR from capabilities"""
        result = colorize("test", Colors.ERROR)
        assert result == "test"


class TestColorConsistency:
    """Test color definition consistency"""

    def test_success_and_add_use_same_green(self):
        """SUCCESS and ADD should use same green color"""
        assert Colors.SUCCESS.rgb == Colors.ADD.rgb

    def test_error_and_remove_use_same_red(self):
        """ERROR and REMOVE should use same red color"""
        assert Colors.ERROR.rgb == Colors.REMOVE.rgb

    def test_warning_and_change_use_same_yellow(self):
        """WARNING and CHANGE should use same yellow color"""
        assert Colors.WARNING.rgb == Colors.CHANGE.rgb


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_string_colorize(self, mock_full_capabilities):
        """colorize() should handle empty strings"""
        result = colorize("", Colors.SUCCESS)
        assert Colors.SUCCESS.code() in result
        assert RESET in result

    def test_multiline_text_colorize(self, mock_full_capabilities):
        """colorize() should handle multiline text"""
        text = "Line 1\nLine 2\nLine 3"
        result = colorize(text, Colors.INFO)
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_special_characters_colorize(self, mock_full_capabilities):
        """colorize() should handle special characters"""
        text = "Test: @#$%^&*(){}[]<>?/"
        result = colorize(text, Colors.WARNING)
        assert text in result.replace(Colors.WARNING.code(), "").replace(RESET, "")
