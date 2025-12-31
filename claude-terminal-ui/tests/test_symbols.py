"""
Tests for symbol token system

Tests cover:
- Symbol class with Unicode and ASCII variants
- Symbol.render() with capability detection
- Symbols library definitions
- Graceful degradation to ASCII
- Force ASCII parameter
"""

import pytest
from unittest.mock import patch
from claude_terminal_ui.core.capabilities import reset_capabilities
from claude_terminal_ui.tokens.symbols import Symbol, Symbols


class TestSymbolClass:
    """Test Symbol dataclass and rendering"""

    def test_symbol_attributes(self):
        """Symbol should have all required attributes"""
        symbol = Symbol("test", "✓", "[OK]")
        assert symbol.name == "test"
        assert symbol.unicode == "✓"
        assert symbol.ascii == "[OK]"

    def test_render_with_unicode_support(self, mock_full_capabilities):
        """render() should return Unicode when supported"""
        symbol = Symbol("test", "✓", "[OK]")
        assert symbol.render() == "✓"

    def test_render_without_unicode_support(self, mock_minimal_capabilities):
        """render() should return ASCII when Unicode not supported"""
        symbol = Symbol("test", "✓", "[OK]")
        assert symbol.render() == "[OK]"

    def test_render_force_ascii_true(self, mock_full_capabilities):
        """render(force_ascii=True) should return ASCII even with Unicode support"""
        symbol = Symbol("test", "✓", "[OK]")
        assert symbol.render(force_ascii=True) == "[OK]"

    def test_render_force_ascii_false(self, mock_minimal_capabilities):
        """render(force_ascii=False) should return Unicode even without support"""
        symbol = Symbol("test", "✓", "[OK]")
        assert symbol.render(force_ascii=False) == "✓"

    def test_render_force_ascii_none(self, mock_full_capabilities):
        """render(force_ascii=None) should use auto-detection"""
        symbol = Symbol("test", "✓", "[OK]")
        # With full capabilities, should return Unicode
        assert symbol.render(force_ascii=None) == "✓"


class TestStatusSymbols:
    """Test status indicator symbols"""

    def test_success_symbol_unicode(self, mock_full_capabilities):
        """SUCCESS symbol should render as Unicode checkmark"""
        assert Symbols.SUCCESS.render() == "\u2714"

    def test_success_symbol_ascii(self, mock_minimal_capabilities):
        """SUCCESS symbol should render as [OK] in ASCII mode"""
        assert Symbols.SUCCESS.render() == "[OK]"

    def test_error_symbol_unicode(self, mock_full_capabilities):
        """ERROR symbol should render as Unicode X"""
        assert Symbols.ERROR.render() == "\u2718"

    def test_error_symbol_ascii(self, mock_minimal_capabilities):
        """ERROR symbol should render as [X] in ASCII mode"""
        assert Symbols.ERROR.render() == "[X]"

    def test_warning_symbol_unicode(self, mock_full_capabilities):
        """WARNING symbol should render as Unicode warning sign"""
        assert Symbols.WARNING.render() == "\u26a0"

    def test_warning_symbol_ascii(self, mock_minimal_capabilities):
        """WARNING symbol should render as [!] in ASCII mode"""
        assert Symbols.WARNING.render() == "[!]"

    def test_info_symbol_unicode(self, mock_full_capabilities):
        """INFO symbol should render as Unicode info symbol"""
        assert Symbols.INFO.render() == "\u2139"

    def test_info_symbol_ascii(self, mock_minimal_capabilities):
        """INFO symbol should render as [i] in ASCII mode"""
        assert Symbols.INFO.render() == "[i]"

    def test_debug_symbol_unicode(self, mock_full_capabilities):
        """DEBUG symbol should render as Unicode gear"""
        assert Symbols.DEBUG.render() == "\u2699"

    def test_debug_symbol_ascii(self, mock_minimal_capabilities):
        """DEBUG symbol should render as [D] in ASCII mode"""
        assert Symbols.DEBUG.render() == "[D]"


class TestProgressSymbols:
    """Test progress indicator symbols"""

    def test_bullet_symbol_unicode(self, mock_full_capabilities):
        """BULLET should render as Unicode bullet point"""
        assert Symbols.BULLET.render() == "\u2022"

    def test_bullet_symbol_ascii(self, mock_minimal_capabilities):
        """BULLET should render as asterisk in ASCII mode"""
        assert Symbols.BULLET.render() == "*"

    def test_arrow_right_unicode(self, mock_full_capabilities):
        """ARROW_RIGHT should render as Unicode arrow"""
        assert Symbols.ARROW_RIGHT.render() == "\u2192"

    def test_arrow_right_ascii(self, mock_minimal_capabilities):
        """ARROW_RIGHT should render as -> in ASCII mode"""
        assert Symbols.ARROW_RIGHT.render() == "->"

    def test_arrow_left_unicode(self, mock_full_capabilities):
        """ARROW_LEFT should render as Unicode arrow"""
        assert Symbols.ARROW_LEFT.render() == "\u2190"

    def test_arrow_left_ascii(self, mock_minimal_capabilities):
        """ARROW_LEFT should render as <- in ASCII mode"""
        assert Symbols.ARROW_LEFT.render() == "<-"

    def test_arrow_up_unicode(self, mock_full_capabilities):
        """ARROW_UP should render as Unicode arrow"""
        assert Symbols.ARROW_UP.render() == "\u2191"

    def test_arrow_up_ascii(self, mock_minimal_capabilities):
        """ARROW_UP should render as ^ in ASCII mode"""
        assert Symbols.ARROW_UP.render() == "^"

    def test_arrow_down_unicode(self, mock_full_capabilities):
        """ARROW_DOWN should render as Unicode arrow"""
        assert Symbols.ARROW_DOWN.render() == "\u2193"

    def test_arrow_down_ascii(self, mock_minimal_capabilities):
        """ARROW_DOWN should render as v in ASCII mode"""
        assert Symbols.ARROW_DOWN.render() == "v"


class TestTaskSymbols:
    """Test task status symbols"""

    def test_task_done_unicode(self, mock_full_capabilities):
        """TASK_DONE should render as Unicode checkmark"""
        assert Symbols.TASK_DONE.render() == "\u2713"

    def test_task_done_ascii(self, mock_minimal_capabilities):
        """TASK_DONE should render as [x] in ASCII mode"""
        assert Symbols.TASK_DONE.render() == "[x]"

    def test_task_todo_unicode(self, mock_full_capabilities):
        """TASK_TODO should render as Unicode ballot box"""
        assert Symbols.TASK_TODO.render() == "\u2610"

    def test_task_todo_ascii(self, mock_minimal_capabilities):
        """TASK_TODO should render as [ ] in ASCII mode"""
        assert Symbols.TASK_TODO.render() == "[ ]"

    def test_task_progress_unicode(self, mock_full_capabilities):
        """TASK_PROGRESS should render as Unicode circle"""
        assert Symbols.TASK_PROGRESS.render() == "\u25cb"

    def test_task_progress_ascii(self, mock_minimal_capabilities):
        """TASK_PROGRESS should render as [~] in ASCII mode"""
        assert Symbols.TASK_PROGRESS.render() == "[~]"


class TestFileOperationSymbols:
    """Test file operation symbols (git-style)"""

    def test_file_add_unicode(self, mock_full_capabilities):
        """FILE_ADD should render as Unicode plus sign"""
        assert Symbols.FILE_ADD.render() == "\u2795"

    def test_file_add_ascii(self, mock_minimal_capabilities):
        """FILE_ADD should render as + in ASCII mode"""
        assert Symbols.FILE_ADD.render() == "+"

    def test_file_remove_unicode(self, mock_full_capabilities):
        """FILE_REMOVE should render as Unicode minus sign"""
        assert Symbols.FILE_REMOVE.render() == "\u2796"

    def test_file_remove_ascii(self, mock_minimal_capabilities):
        """FILE_REMOVE should render as - in ASCII mode"""
        assert Symbols.FILE_REMOVE.render() == "-"

    def test_file_modify_unicode(self, mock_full_capabilities):
        """FILE_MODIFY should render as Unicode pencil"""
        assert Symbols.FILE_MODIFY.render() == "\u270e"

    def test_file_modify_ascii(self, mock_minimal_capabilities):
        """FILE_MODIFY should render as * in ASCII mode"""
        assert Symbols.FILE_MODIFY.render() == "*"


class TestTreeSymbols:
    """Test tree structure symbols"""

    def test_tree_branch_unicode(self, mock_full_capabilities):
        """TREE_BRANCH should render as Unicode box drawing"""
        assert Symbols.TREE_BRANCH.render() == "\u251c\u2500\u2500"

    def test_tree_branch_ascii(self, mock_minimal_capabilities):
        """TREE_BRANCH should render as |-- in ASCII mode"""
        assert Symbols.TREE_BRANCH.render() == "|--"

    def test_tree_last_unicode(self, mock_full_capabilities):
        """TREE_LAST should render as Unicode box drawing"""
        assert Symbols.TREE_LAST.render() == "\u2514\u2500\u2500"

    def test_tree_last_ascii(self, mock_minimal_capabilities):
        """TREE_LAST should render as `-- in ASCII mode"""
        assert Symbols.TREE_LAST.render() == "`--"

    def test_tree_pipe_unicode(self, mock_full_capabilities):
        """TREE_PIPE should render as Unicode vertical line"""
        assert Symbols.TREE_PIPE.render() == "\u2502"

    def test_tree_pipe_ascii(self, mock_minimal_capabilities):
        """TREE_PIPE should render as | in ASCII mode"""
        assert Symbols.TREE_PIPE.render() == "|"

    def test_tree_space_consistent(self, mock_full_capabilities):
        """TREE_SPACE should be same in Unicode and ASCII"""
        assert Symbols.TREE_SPACE.render() == "   "


class TestBoxSymbols:
    """Test box drawing symbols"""

    def test_box_corners_unicode(self, mock_full_capabilities):
        """Box corners should render as Unicode box drawing"""
        assert Symbols.BOX_TOP_LEFT.render() == "\u250c"
        assert Symbols.BOX_TOP_RIGHT.render() == "\u2510"
        assert Symbols.BOX_BOTTOM_LEFT.render() == "\u2514"
        assert Symbols.BOX_BOTTOM_RIGHT.render() == "\u2518"

    def test_box_corners_ascii(self, mock_minimal_capabilities):
        """Box corners should render as + in ASCII mode"""
        assert Symbols.BOX_TOP_LEFT.render() == "+"
        assert Symbols.BOX_TOP_RIGHT.render() == "+"
        assert Symbols.BOX_BOTTOM_LEFT.render() == "+"
        assert Symbols.BOX_BOTTOM_RIGHT.render() == "+"

    def test_box_lines_unicode(self, mock_full_capabilities):
        """Box lines should render as Unicode box drawing"""
        assert Symbols.BOX_HORIZONTAL.render() == "\u2500"
        assert Symbols.BOX_VERTICAL.render() == "\u2502"

    def test_box_lines_ascii(self, mock_minimal_capabilities):
        """Box lines should render as - and | in ASCII mode"""
        assert Symbols.BOX_HORIZONTAL.render() == "-"
        assert Symbols.BOX_VERTICAL.render() == "|"

    def test_box_cross_unicode(self, mock_full_capabilities):
        """BOX_CROSS should render as Unicode cross"""
        assert Symbols.BOX_CROSS.render() == "\u253c"

    def test_box_cross_ascii(self, mock_minimal_capabilities):
        """BOX_CROSS should render as + in ASCII mode"""
        assert Symbols.BOX_CROSS.render() == "+"


class TestProgressBarSymbols:
    """Test progress bar block symbols"""

    def test_progress_full_unicode(self, mock_full_capabilities):
        """PROGRESS_FULL should render as Unicode full block"""
        assert Symbols.PROGRESS_FULL.render() == "\u2588"

    def test_progress_full_ascii(self, mock_minimal_capabilities):
        """PROGRESS_FULL should render as # in ASCII mode"""
        assert Symbols.PROGRESS_FULL.render() == "#"

    def test_progress_partial_unicode(self, mock_full_capabilities):
        """PROGRESS_PARTIAL should render as Unicode medium shade"""
        assert Symbols.PROGRESS_PARTIAL.render() == "\u2592"

    def test_progress_partial_ascii(self, mock_minimal_capabilities):
        """PROGRESS_PARTIAL should render as = in ASCII mode"""
        assert Symbols.PROGRESS_PARTIAL.render() == "="

    def test_progress_empty_unicode(self, mock_full_capabilities):
        """PROGRESS_EMPTY should render as Unicode light shade"""
        assert Symbols.PROGRESS_EMPTY.render() == "\u2591"

    def test_progress_empty_ascii(self, mock_minimal_capabilities):
        """PROGRESS_EMPTY should render as - in ASCII mode"""
        assert Symbols.PROGRESS_EMPTY.render() == "-"


class TestSpinnerFrames:
    """Test spinner animation frames"""

    def test_spinner_frames_exist(self):
        """SPINNER_FRAMES should be a list of Symbol objects"""
        assert isinstance(Symbols.SPINNER_FRAMES, list)
        assert len(Symbols.SPINNER_FRAMES) > 0
        assert all(isinstance(s, Symbol) for s in Symbols.SPINNER_FRAMES)

    def test_spinner_frames_count(self):
        """SPINNER_FRAMES should have 8 frames"""
        assert len(Symbols.SPINNER_FRAMES) == 8

    def test_spinner_frames_unicode(self, mock_full_capabilities):
        """Spinner frames should use Unicode braille patterns"""
        frames = [s.render() for s in Symbols.SPINNER_FRAMES]
        # Should have Unicode braille characters
        assert all(isinstance(f, str) for f in frames)
        assert len(set(frames)) == 8  # All unique

    def test_spinner_frames_ascii(self, mock_minimal_capabilities):
        """Spinner frames should use |/-\\ in ASCII mode"""
        frames = [s.render() for s in Symbols.SPINNER_FRAMES]
        # Should only use ASCII characters
        assert all(c in "|/-\\" for c in frames)


class TestMiscSymbols:
    """Test miscellaneous symbols"""

    def test_star_unicode(self, mock_full_capabilities):
        """STAR should render as Unicode black star"""
        assert Symbols.STAR.render() == "\u2605"

    def test_star_ascii(self, mock_minimal_capabilities):
        """STAR should render as * in ASCII mode"""
        assert Symbols.STAR.render() == "*"

    def test_heart_unicode(self, mock_full_capabilities):
        """HEART should render as Unicode heart"""
        assert Symbols.HEART.render() == "\u2665"

    def test_heart_ascii(self, mock_minimal_capabilities):
        """HEART should render as <3 in ASCII mode"""
        assert Symbols.HEART.render() == "<3"

    def test_lightning_unicode(self, mock_full_capabilities):
        """LIGHTNING should render as Unicode lightning bolt"""
        assert Symbols.LIGHTNING.render() == "\u26a1"

    def test_lightning_ascii(self, mock_minimal_capabilities):
        """LIGHTNING should render as ! in ASCII mode"""
        assert Symbols.LIGHTNING.render() == "!"

    def test_clock_unicode(self, mock_full_capabilities):
        """CLOCK should render as Unicode clock"""
        assert Symbols.CLOCK.render() == "\u23f0"

    def test_clock_ascii(self, mock_minimal_capabilities):
        """CLOCK should render as @ in ASCII mode"""
        assert Symbols.CLOCK.render() == "@"

    def test_folder_unicode(self, mock_full_capabilities):
        """FOLDER should render as Unicode folder emoji"""
        assert Symbols.FOLDER.render() == "\U0001f4c1"

    def test_folder_ascii(self, mock_minimal_capabilities):
        """FOLDER should render as [D] in ASCII mode"""
        assert Symbols.FOLDER.render() == "[D]"

    def test_file_unicode(self, mock_full_capabilities):
        """FILE should render as Unicode file emoji"""
        assert Symbols.FILE.render() == "\U0001f4c4"

    def test_file_ascii(self, mock_minimal_capabilities):
        """FILE should render as [F] in ASCII mode"""
        assert Symbols.FILE.render() == "[F]"


class TestSymbolConsistency:
    """Test symbol definition consistency"""

    def test_all_symbols_have_names(self):
        """All symbols should have unique names"""
        names = set()
        for attr_name in dir(Symbols):
            attr = getattr(Symbols, attr_name)
            if isinstance(attr, Symbol):
                assert attr.name not in names, f"Duplicate name: {attr.name}"
                names.add(attr.name)

    def test_all_symbols_have_both_variants(self):
        """All symbols should have both Unicode and ASCII variants"""
        for attr_name in dir(Symbols):
            attr = getattr(Symbols, attr_name)
            if isinstance(attr, Symbol):
                assert attr.unicode is not None
                assert attr.ascii is not None
                assert len(attr.unicode) > 0
                assert len(attr.ascii) > 0


class TestSymbolDegradation:
    """Test graceful degradation scenarios"""

    def test_degradation_with_256_color(self, mock_256_color):
        """Symbols should use Unicode with 256-color terminals"""
        # 256-color typically supports UTF-8
        assert Symbols.SUCCESS.render() == "\u2714"

    def test_degradation_with_basic_color(self, mock_basic_color):
        """Symbols should use ASCII with basic color terminals (no UTF-8)"""
        # Basic color without UTF-8 (cp437 encoding)
        assert Symbols.SUCCESS.render() == "[OK]"

    def test_degradation_windows_terminal(self, mock_windows_terminal):
        """Windows Terminal should support Unicode symbols"""
        assert Symbols.SUCCESS.render() == "\u2714"

    def test_degradation_iterm2(self, mock_iterm2):
        """iTerm2 should support Unicode symbols"""
        assert Symbols.SUCCESS.render() == "\u2714"


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_empty_unicode_fallback(self):
        """Symbol with empty Unicode should still work"""
        symbol = Symbol("test", "", "[FALLBACK]")
        # Should return ASCII when Unicode is empty
        assert symbol.render(force_ascii=False) == ""

    def test_empty_ascii_fallback(self):
        """Symbol with empty ASCII should still work"""
        symbol = Symbol("test", "✓", "")
        assert symbol.render(force_ascii=True) == ""

    def test_multichar_unicode_symbol(self, mock_full_capabilities):
        """Symbols can have multi-character Unicode (e.g., box drawing)"""
        # TREE_BRANCH is 3 characters
        result = Symbols.TREE_BRANCH.render()
        assert len(result) == 3
        assert result == "\u251c\u2500\u2500"

    def test_multichar_ascii_symbol(self, mock_minimal_capabilities):
        """Symbols can have multi-character ASCII"""
        # TREE_BRANCH ASCII is 3 characters
        result = Symbols.TREE_BRANCH.render()
        assert len(result) == 3
        assert result == "|--"
