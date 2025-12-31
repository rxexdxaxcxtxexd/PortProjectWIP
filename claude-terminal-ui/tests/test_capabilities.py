"""
Tests for terminal capability detection system

Tests cover:
- Color support detection (none, 16, 256, truecolor)
- Unicode/encoding detection (UTF-8 vs legacy encodings)
- Terminal dimensions
- Interactive vs non-interactive detection
- Terminal emulator identification
- Hyperlink support detection
- Environment variable precedence
"""

import os
import sys
from unittest.mock import patch, MagicMock
import pytest
from claude_terminal_ui.core.capabilities import (
    ColorSupport,
    TerminalCapabilities,
    CapabilityDetector,
    get_capabilities,
    reset_capabilities,
)


class TestColorSupportDetection:
    """Test color support level detection"""

    def test_no_color_env_forces_none(self):
        """NO_COLOR environment variable should disable all colors"""
        with patch.dict("os.environ", {"NO_COLOR": "1"}):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.NONE

    def test_force_color_3_gives_truecolor(self):
        """FORCE_COLOR=3 should enable truecolor"""
        with patch.dict("os.environ", {"FORCE_COLOR": "3"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.TRUECOLOR

    def test_force_color_true_gives_truecolor(self):
        """FORCE_COLOR=true should enable truecolor"""
        with patch.dict("os.environ", {"FORCE_COLOR": "true"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.TRUECOLOR

    def test_force_color_1_gives_basic(self):
        """FORCE_COLOR=1 should enable basic colors"""
        with patch.dict("os.environ", {"FORCE_COLOR": "1"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.BASIC

    def test_wt_session_gives_truecolor(self):
        """Windows Terminal (WT_SESSION) should enable truecolor"""
        with patch.dict("os.environ", {"WT_SESSION": "abc123"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.TRUECOLOR

    def test_colorterm_truecolor(self):
        """COLORTERM=truecolor should enable truecolor"""
        with patch.dict("os.environ", {"COLORTERM": "truecolor"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.TRUECOLOR

    def test_colorterm_24bit(self):
        """COLORTERM=24bit should enable truecolor"""
        with patch.dict("os.environ", {"COLORTERM": "24bit"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.TRUECOLOR

    def test_term_256color_gives_extended(self):
        """TERM=xterm-256color should enable 256 colors"""
        with patch.dict("os.environ", {"TERM": "xterm-256color"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.EXTENDED

    def test_term_xterm_gives_basic(self):
        """TERM=xterm should enable basic 16 colors"""
        with patch.dict("os.environ", {"TERM": "xterm"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.BASIC

    def test_term_vt100_gives_basic(self):
        """TERM=vt100 should enable basic colors"""
        with patch.dict("os.environ", {"TERM": "vt100"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.BASIC

    def test_term_screen_gives_basic(self):
        """TERM=screen should enable basic colors"""
        with patch.dict("os.environ", {"TERM": "screen"}, clear=True):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.BASIC

    def test_isatty_fallback(self):
        """If stdout is a tty and no env vars set, use basic color"""
        with patch.dict("os.environ", {}, clear=True):
            mock_stdout = MagicMock()
            mock_stdout.isatty.return_value = True
            with patch("sys.stdout", mock_stdout):
                reset_capabilities()
                caps = get_capabilities()
                assert caps.color_support == ColorSupport.BASIC

    def test_non_tty_no_color(self):
        """If stdout is not a tty, no color support"""
        with patch.dict("os.environ", {}, clear=True):
            mock_stdout = MagicMock()
            mock_stdout.isatty.return_value = False
            with patch("sys.stdout", mock_stdout):
                reset_capabilities()
                caps = get_capabilities()
                assert caps.color_support == ColorSupport.NONE

    def test_no_color_overrides_force_color(self):
        """NO_COLOR should take precedence over FORCE_COLOR"""
        with patch.dict("os.environ", {"NO_COLOR": "1", "FORCE_COLOR": "3"}):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.color_support == ColorSupport.NONE


class TestUnicodeSupportDetection:
    """Test Unicode/UTF-8 encoding detection"""

    def test_utf8_encoding_returns_true(self):
        """sys.stdout.encoding = 'utf-8' should enable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "utf-8"
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is True

    def test_utf_8_uppercase_returns_true(self):
        """sys.stdout.encoding = 'UTF-8' should enable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "UTF-8"
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is True

    def test_cp1252_returns_false(self):
        """sys.stdout.encoding = 'cp1252' should disable Unicode (Windows edge case)"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "cp1252"
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False

    def test_cp437_returns_false(self):
        """sys.stdout.encoding = 'cp437' (DOS) should disable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "cp437"
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False

    def test_ascii_returns_false(self):
        """sys.stdout.encoding = 'ascii' should disable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "ascii"
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False

    def test_empty_encoding_returns_false(self):
        """Empty encoding string should disable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = ""
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False

    def test_none_encoding_returns_false(self):
        """None encoding should disable Unicode"""
        mock_stdout = MagicMock()
        mock_stdout.encoding = None
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False

    def test_no_encoding_attr_returns_false(self):
        """Missing encoding attribute should disable Unicode"""
        mock_stdout = MagicMock(spec=[])  # No encoding attribute
        with patch("sys.stdout", mock_stdout):
            assert CapabilityDetector._detect_unicode_support() is False


class TestTerminalDimensions:
    """Test terminal width and height detection"""

    def test_detect_width_success(self):
        """Should detect terminal width from os.get_terminal_size()"""
        with patch(
            "os.get_terminal_size", return_value=type("size", (), {"columns": 120, "lines": 40})()
        ):
            assert CapabilityDetector._detect_width() == 120

    def test_detect_height_success(self):
        """Should detect terminal height from os.get_terminal_size()"""
        with patch(
            "os.get_terminal_size", return_value=type("size", (), {"columns": 120, "lines": 40})()
        ):
            assert CapabilityDetector._detect_height() == 40

    def test_width_fallback_on_oserror(self):
        """Should fallback to 80 width on OSError"""
        with patch("os.get_terminal_size", side_effect=OSError("not a terminal")):
            assert CapabilityDetector._detect_width() == 80

    def test_height_fallback_on_oserror(self):
        """Should fallback to 24 height on OSError"""
        with patch("os.get_terminal_size", side_effect=OSError("not a terminal")):
            assert CapabilityDetector._detect_height() == 24

    def test_width_fallback_on_valueerror(self):
        """Should fallback to 80 width on ValueError"""
        with patch("os.get_terminal_size", side_effect=ValueError("invalid")):
            assert CapabilityDetector._detect_width() == 80

    def test_height_fallback_on_valueerror(self):
        """Should fallback to 24 height on ValueError"""
        with patch("os.get_terminal_size", side_effect=ValueError("invalid")):
            assert CapabilityDetector._detect_height() == 24


class TestInteractiveDetection:
    """Test interactive terminal detection"""

    def test_both_stdin_stdout_tty_is_interactive(self):
        """Both stdin and stdout are ttys = interactive"""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdin", mock_stdin):
            with patch("sys.stdout", mock_stdout):
                assert CapabilityDetector._detect_interactive() is True

    def test_stdin_not_tty_is_not_interactive(self):
        """stdin not a tty (piped input) = not interactive"""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdin", mock_stdin):
            with patch("sys.stdout", mock_stdout):
                assert CapabilityDetector._detect_interactive() is False

    def test_stdout_not_tty_is_not_interactive(self):
        """stdout not a tty (redirected output) = not interactive"""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False

        with patch("sys.stdin", mock_stdin):
            with patch("sys.stdout", mock_stdout):
                assert CapabilityDetector._detect_interactive() is False

    def test_no_isatty_method_is_not_interactive(self):
        """Missing isatty() method = not interactive"""
        mock_stdin = MagicMock(spec=[])  # No isatty
        mock_stdout = MagicMock(spec=[])

        with patch("sys.stdin", mock_stdin):
            with patch("sys.stdout", mock_stdout):
                assert CapabilityDetector._detect_interactive() is False


class TestTerminalNameDetection:
    """Test terminal emulator identification"""

    def test_windows_terminal_detection(self):
        """WT_SESSION should identify as Windows Terminal"""
        with patch.dict("os.environ", {"WT_SESSION": "abc123"}):
            assert CapabilityDetector._detect_terminal_name() == "Windows Terminal"

    def test_iterm2_detection(self):
        """TERM_PROGRAM=iTerm.app should identify as iTerm2"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "iTerm.app"}, clear=True):
            assert CapabilityDetector._detect_terminal_name() == "iTerm2"

    def test_apple_terminal_detection(self):
        """TERM_PROGRAM=Apple_Terminal should identify as Terminal.app"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "Apple_Terminal"}, clear=True):
            assert CapabilityDetector._detect_terminal_name() == "Terminal.app"

    def test_vscode_detection(self):
        """TERM_PROGRAM=vscode should identify as VS Code"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "vscode"}, clear=True):
            assert CapabilityDetector._detect_terminal_name() == "VS Code"

    def test_fallback_to_term_variable(self):
        """Should fallback to TERM variable if no specific terminal detected"""
        with patch.dict("os.environ", {"TERM": "xterm-256color"}, clear=True):
            assert CapabilityDetector._detect_terminal_name() == "xterm-256color"

    def test_unknown_terminal(self):
        """Should return 'unknown' if no terminal info available"""
        with patch.dict("os.environ", {}, clear=True):
            assert CapabilityDetector._detect_terminal_name() == "unknown"


class TestHyperlinkDetection:
    """Test OSC 8 hyperlink support detection"""

    def test_iterm2_supports_hyperlinks(self):
        """iTerm2 should support hyperlinks"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "iTerm.app"}):
            assert CapabilityDetector._detect_hyperlinks() is True

    def test_wezterm_supports_hyperlinks(self):
        """WezTerm should support hyperlinks"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "WezTerm"}):
            assert CapabilityDetector._detect_hyperlinks() is True

    def test_hyper_supports_hyperlinks(self):
        """Hyper terminal should support hyperlinks"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "Hyper"}):
            assert CapabilityDetector._detect_hyperlinks() is True

    def test_windows_terminal_supports_hyperlinks(self):
        """Windows Terminal should support hyperlinks"""
        with patch.dict("os.environ", {"WT_SESSION": "test"}, clear=True):
            assert CapabilityDetector._detect_hyperlinks() is True

    def test_vscode_no_hyperlink_support(self):
        """VS Code terminal should not support hyperlinks"""
        with patch.dict("os.environ", {"TERM_PROGRAM": "vscode"}, clear=True):
            assert CapabilityDetector._detect_hyperlinks() is False

    def test_unknown_terminal_no_hyperlinks(self):
        """Unknown terminal should not support hyperlinks"""
        with patch.dict("os.environ", {}, clear=True):
            assert CapabilityDetector._detect_hyperlinks() is False


class TestPlatformDetection:
    """Test platform/OS detection"""

    def test_windows_detection(self):
        """Should detect Windows platform"""
        with patch("platform.system", return_value="Windows"):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.is_windows is True

    def test_linux_detection(self):
        """Should detect non-Windows (Linux)"""
        with patch("platform.system", return_value="Linux"):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.is_windows is False

    def test_darwin_detection(self):
        """Should detect non-Windows (macOS)"""
        with patch("platform.system", return_value="Darwin"):
            reset_capabilities()
            caps = get_capabilities()
            assert caps.is_windows is False


class TestFixtureIntegration:
    """Test integration with test fixtures"""

    def test_full_capabilities_fixture(self, mock_full_capabilities):
        """Test full capabilities fixture provides expected values"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.TRUECOLOR
        assert caps.unicode_support is True
        assert caps.is_interactive is True
        assert caps.width == 100
        assert caps.height == 30
        assert caps.terminal_name == "Windows Terminal"
        assert caps.supports_hyperlinks is True

    def test_minimal_capabilities_fixture(self, mock_minimal_capabilities):
        """Test minimal capabilities fixture (cp1252 edge case)"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.NONE
        assert caps.unicode_support is False  # Critical: cp1252 should disable Unicode
        assert caps.is_interactive is False
        assert caps.width == 80  # Fallback
        assert caps.height == 24  # Fallback

    def test_basic_color_fixture(self, mock_basic_color):
        """Test basic color fixture"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.BASIC
        assert caps.unicode_support is False  # cp437 encoding

    def test_256_color_fixture(self, mock_256_color):
        """Test 256-color fixture"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.EXTENDED
        assert caps.unicode_support is True

    def test_windows_terminal_fixture(self, mock_windows_terminal):
        """Test Windows Terminal fixture"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.TRUECOLOR
        assert caps.terminal_name == "Windows Terminal"
        assert caps.supports_hyperlinks is True

    def test_iterm2_fixture(self, mock_iterm2):
        """Test iTerm2 fixture"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.TRUECOLOR
        assert caps.terminal_name == "iTerm2"
        assert caps.supports_hyperlinks is True
        assert caps.is_windows is False

    def test_vscode_fixture(self, mock_vscode_terminal):
        """Test VS Code terminal fixture"""
        caps = get_capabilities()
        assert caps.color_support == ColorSupport.TRUECOLOR
        assert caps.terminal_name == "VS Code"
        assert caps.supports_hyperlinks is False


class TestCapabilitiesCaching:
    """Test capabilities singleton caching"""

    def test_capabilities_cached(self):
        """Should cache capabilities and return same instance"""
        reset_capabilities()
        caps1 = get_capabilities()
        caps2 = get_capabilities()
        assert caps1 is caps2

    def test_reset_clears_cache(self):
        """reset_capabilities() should clear cache"""
        caps1 = get_capabilities()
        reset_capabilities()
        caps2 = get_capabilities()
        assert caps1 is not caps2


class TestTerminalCapabilitiesDataclass:
    """Test TerminalCapabilities dataclass properties"""

    def test_immutable_dataclass(self):
        """TerminalCapabilities should be frozen/immutable"""
        caps = TerminalCapabilities(
            color_support=ColorSupport.BASIC,
            unicode_support=True,
            width=80,
            height=24,
            is_interactive=True,
            is_windows=False,
            terminal_name="xterm",
            supports_hyperlinks=False,
        )
        with pytest.raises(AttributeError):
            caps.width = 100  # Should raise error (frozen dataclass)

    def test_all_fields_present(self):
        """TerminalCapabilities should have all expected fields"""
        caps = get_capabilities()
        assert hasattr(caps, "color_support")
        assert hasattr(caps, "unicode_support")
        assert hasattr(caps, "width")
        assert hasattr(caps, "height")
        assert hasattr(caps, "is_interactive")
        assert hasattr(caps, "is_windows")
        assert hasattr(caps, "terminal_name")
        assert hasattr(caps, "supports_hyperlinks")
