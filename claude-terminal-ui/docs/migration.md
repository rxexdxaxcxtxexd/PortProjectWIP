# Migration Guide

## Migrating from Raw print() Statements

This guide helps you migrate existing scripts to use the `claude-terminal-ui` design system.

## Quick Start

### Before
```python
print("="*70)
print(" "*20 + "UNIFIED CHECKPOINT")
print("="*70)
print("[OK] Session saved")
print("[ERROR] Failed to save checkpoint")
```

### After
```python
import claude_terminal_ui as ui

ui.header("UNIFIED CHECKPOINT")
ui.print_success("Session saved")
ui.print_error("Failed to save checkpoint")
```

## Component Mapping

### Status Messages

| Old Pattern | New Function | Output |
|------------|--------------|--------|
| `print("[OK] ...")` | `ui.print_success("...")` | ✓ or [OK] |
| `print("[ERROR] ...")` | `ui.print_error("...")` | ✗ or [X] |
| `print("[WARNING] ...")` | `ui.print_warning("...")` | ⚠ or [!] |
| `print("[INFO] ...")` | `ui.print_info("...")` | ℹ or [i] |
| `print("[DEBUG] ...")` | `ui.print_debug("...")` | ⚙ or [D] |

### Headers and Dividers

| Old Pattern | New Function |
|------------|--------------|
| `print("="*70)` | `ui.header("TITLE")` |
| `print("-"*70)` | `ui.divider()` |
| `print("--- Step 1 ---")` | `ui.divider(label="Step 1")` |

### Progress Indicators

| Old Pattern | New Function |
|------------|--------------|
| `print("[1/3] ...")` | `ui.step_indicator(1, 3, "...")` |
| ASCII progress bar | `ui.progress_bar(current, total)` |
| No spinner support | `with ui.spinner("Loading"): ...` |

## Migration Checklist

For each script you're migrating:

- [ ] Add import: `import claude_terminal_ui as ui`
- [ ] Replace status tags (`[OK]`, `[ERROR]`, etc.)
- [ ] Replace header formatting
- [ ] Replace progress indicators
- [ ] Test output on Windows and Unix
- [ ] Verify colors appear correctly
- [ ] Check ASCII fallbacks work

## Example: checkpoint.py Migration

### Before (excerpt)
```python
def main():
    print("="*70)
    print(" "*20 + "UNIFIED CHECKPOINT")
    print("="*70)
    print()

    print("[1/3] Collecting and saving session data...")
    success = save_session()

    if success:
        print("[OK] Session saved")
    else:
        print("[ERROR] Failed to save session")
        sys.exit(1)

    print("[2/3] Updating CLAUDE.md...")
    # ...
```

### After
```python
import claude_terminal_ui as ui

def main():
    ui.header("UNIFIED CHECKPOINT")
    print()

    print(ui.step_indicator(1, 3, "Collecting and saving session data..."))
    success = save_session()

    if success:
        ui.print_success("Session saved")
    else:
        ui.print_error("Failed to save session")
        sys.exit(1)

    print(ui.step_indicator(2, 3, "Updating CLAUDE.md..."))
    # ...
```

## Advanced: Custom Styling

### Using Colors Directly
```python
from claude_terminal_ui.tokens import Colors, colorize

colored_text = colorize("Important!", Colors.WARNING, bold=True)
print(colored_text)
```

### Custom Header Width
```python
# For wide audit reports
ui.header("AUDIT REPORT", width=100)
```

## Backward Compatibility

If you need gradual migration, the old patterns still work:
```python
import claude_terminal_ui as ui

# Old code still works
print("[OK] This still works")

# But you can mix with new:
ui.print_success("And this is better!")
```

## Testing Your Migration

1. **Visual Test**: Run your script and verify colors appear
2. **Windows Test**: Test on Windows with cp1252 encoding
3. **Redirect Test**: Test with redirected output (`python script.py > out.txt`)
4. **No Color Test**: Set `NO_COLOR=1` and verify ASCII fallbacks

## Common Pitfalls

### ❌ Don't hardcode Unicode
```python
# Bad - will fail on Windows cp1252
print("✓ Success!")

# Good - uses automatic detection
ui.print_success("Success!")
```

### ❌ Don't mix formatting approaches
```python
# Inconsistent
print("="*70)
ui.header("TITLE")
print("="*70)

# Better
ui.header("TITLE")
```

### ✅ Do use consistent widths
```python
# All 70 chars (standardized)
ui.header("TITLE")
ui.divider()
ui.subheader("Subsection")
```

## Getting Help

- **API Reference**: See `docs/api-reference.md`
- **Examples**: Check `examples/demo_all.py`
- **Issues**: Report at GitHub repository
