"""
Shared test fixtures for claude-terminal-ui

Provides reusable fixtures for testing terminal capabilities,
color support, and Unicode rendering across different environments.
"""

import sys
from typing import Any, Generator
from unittest.mock import Mock, MagicMock, patch
import pytest


@pytest.fixture
def mock_full_capabilities():
    """
    Mock environment with full terminal capabilities:
    - Truecolor (24-bit RGB) support
    - Unicode/UTF-8 encoding
    - Interactive terminal
    - 100x30 dimensions
    - Windows Terminal
    """
    with patch.dict(
        "os.environ",
        {
            "WT_SESSION": "abc123",
            "COLORTERM": "truecolor",
            "TERM": "xterm-256color",
        },
        clear=False,
    ):
        # Mock sys.stdout with UTF-8 encoding
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "utf-8"

        # Mock sys.stdin
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        # Mock terminal size
        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 100, "lines": 30})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Windows"):
                        # Reset capabilities cache
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture
def mock_minimal_capabilities():
    """
    Mock environment with minimal terminal capabilities:
    - No color support (NO_COLOR set)
    - cp1252 encoding (Windows legacy)
    - Non-interactive (piped/redirected)
    - Default 80x24 dimensions
    """
    with patch.dict(
        "os.environ",
        {
            "NO_COLOR": "1",
            "TERM": "dumb",
        },
        clear=True,
    ):
        # Mock sys.stdout with cp1252 encoding (Windows legacy)
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False
        mock_stdout.encoding = "cp1252"

        # Mock sys.stdin
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False

        # Mock terminal size to raise OSError (no terminal)
        with patch("os.get_terminal_size", side_effect=OSError("not a terminal")):
            # Patch sys.stdout in both sys module and capabilities module
            with patch("sys.stdout", mock_stdout):
                with patch("claude_terminal_ui.core.capabilities.sys.stdout", mock_stdout):
                    with patch("sys.stdin", mock_stdin):
                        with patch("platform.system", return_value="Windows"):
                            # Reset capabilities cache
                            from claude_terminal_ui.core.capabilities import reset_capabilities
                            reset_capabilities()
                            yield


@pytest.fixture
def mock_basic_color():
    """
    Mock environment with basic 16-color support:
    - 16 ANSI colors only
    - No Unicode (ASCII fallback)
    - Interactive terminal
    """
    with patch.dict(
        "os.environ",
        {
            "TERM": "xterm",
        },
        clear=True,
    ):
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "cp437"  # DOS encoding, no UTF-8

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 80, "lines": 24})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Windows"):
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture
def mock_256_color():
    """
    Mock environment with 256-color support:
    - 256 ANSI colors
    - UTF-8 Unicode support
    - Interactive terminal
    """
    with patch.dict(
        "os.environ",
        {
            "TERM": "xterm-256color",
        },
        clear=True,
    ):
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "utf-8"

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 120, "lines": 40})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Linux"):
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture
def mock_windows_terminal():
    """
    Mock Windows Terminal environment:
    - Truecolor support
    - UTF-8 encoding
    - Hyperlink support
    """
    with patch.dict(
        "os.environ",
        {
            "WT_SESSION": "test-session-id",
            "COLORTERM": "truecolor",
        },
        clear=True,
    ):
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "utf-8"

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 120, "lines": 30})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Windows"):
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture
def mock_iterm2():
    """
    Mock iTerm2 environment (macOS):
    - Truecolor support
    - UTF-8 encoding
    - Hyperlink support
    """
    with patch.dict(
        "os.environ",
        {
            "TERM_PROGRAM": "iTerm.app",
            "COLORTERM": "truecolor",
        },
        clear=True,
    ):
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "utf-8"

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 140, "lines": 50})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Darwin"):
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture
def mock_vscode_terminal():
    """
    Mock VS Code integrated terminal:
    - Truecolor support
    - UTF-8 encoding
    - No hyperlink support
    """
    with patch.dict(
        "os.environ",
        {
            "TERM_PROGRAM": "vscode",
            "COLORTERM": "truecolor",
        },
        clear=True,
    ):
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True
        mock_stdout.encoding = "utf-8"

        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True

        with patch("os.get_terminal_size", return_value=type("size", (), {"columns": 100, "lines": 30})()):
            with patch("sys.stdout", mock_stdout):
                with patch("sys.stdin", mock_stdin):
                    with patch("platform.system", return_value="Windows"):
                        from claude_terminal_ui.core.capabilities import reset_capabilities
                        reset_capabilities()
                        yield


@pytest.fixture(autouse=True)
def reset_caps_after_test():
    """Automatically reset capabilities cache before and after each test"""
    from claude_terminal_ui.core.capabilities import reset_capabilities
    reset_capabilities()  # Reset before test to ensure clean state
    yield
    reset_capabilities()  # Reset after test to clean up
