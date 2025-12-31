# Migration Quick Reference Card

**For migrating scripts to claude-terminal-ui design system**

---

## Setup (Copy to top of script)

```python
# Import the UI design system
try:
    import claude_terminal_ui as ui
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    # Fallback functions if UI not available
    class ui:
        @staticmethod
        def header(title, **kwargs):
            print("=" * 70)
            print(" " * ((70 - len(title)) // 2) + title)
            print("=" * 70)

        @staticmethod
        def divider(**kwargs):
            print("-" * 70)

        @staticmethod
        def step_indicator(current, total, message=""):
            return f"[{current}/{total}] {message}"

        @staticmethod
        def print_success(message, **kwargs):
            print(f"[OK] {message}")

        @staticmethod
        def print_error(message, **kwargs):
            print(f"[ERROR] {message}")

        @staticmethod
        def print_warning(message, **kwargs):
            print(f"[WARNING] {message}")

        @staticmethod
        def print_info(message, **kwargs):
            print(f"[INFO] {message}")
```

---

## Quick Replacements

### Status Messages
```python
# BEFORE → AFTER

print("[OK] Success")          → ui.print_success("Success")
print("[ERROR] Failed")        → ui.print_error("Failed")
print("[WARNING] Watch out")   → ui.print_warning("Watch out")
print("[INFO] Note this")      → ui.print_info("Note this")
print("[DEBUG] Debugging")     → ui.print_debug("Debugging")
```

### Headers
```python
# BEFORE → AFTER

print("="*70)                  → print(ui.header("TITLE"))
print(" "*20 + "TITLE")
print("="*70)

print("-"*70)                  → print(ui.divider())

print("--- Label ---")         → print(ui.divider(label="Label"))
print("-"*60)
```

### Progress Indicators
```python
# BEFORE → AFTER

print("[1/3] Step one")        → print(ui.step_indicator(1, 3, "Step one"))
print(f"[{i}/{total}] Task")   → print(ui.step_indicator(i, total, "Task"))
```

---

## Migration Checklist

- [ ] Add UI import with fallback (see Setup above)
- [ ] Replace all `[OK]` → `ui.print_success()`
- [ ] Replace all `[ERROR]` → `ui.print_error()`
- [ ] Replace all `[WARNING]` → `ui.print_warning()`
- [ ] Replace all `[INFO]` → `ui.print_info()`
- [ ] Replace header blocks → `ui.header()`
- [ ] Replace divider lines → `ui.divider()`
- [ ] Replace `[X/Y]` → `ui.step_indicator(X, Y, ...)`
- [ ] Test script runs without errors
- [ ] Test with UI library installed
- [ ] Test WITHOUT UI library (fallback)
- [ ] Test with NO_COLOR=1 (no colors)
- [ ] Test redirected output (pipe to file)
- [ ] Update migration docs

---

## Common Patterns

### Pattern 1: Multi-line header
```python
# BEFORE
print("="*70)
print(" "*15 + "VERY LONG HEADER TITLE")
print("="*70)

# AFTER
print(ui.header("VERY LONG HEADER TITLE"))
```

### Pattern 2: Conditional messages
```python
# BEFORE
if success:
    print("[OK] Done")
else:
    print("[ERROR] Failed")

# AFTER
if success:
    ui.print_success("Done")
else:
    ui.print_error("Failed")
```

### Pattern 3: Section with divider
```python
# BEFORE
print("-" * 70)
print("Results:")
print("-" * 70)

# AFTER
print(ui.divider(label="Results"))
# or
print(ui.subheader("Results"))
```

### Pattern 4: Progress loop
```python
# BEFORE
for i, item in enumerate(items, 1):
    print(f"[{i}/{total}] Processing {item}")

# AFTER
for i, item in enumerate(items, 1):
    print(ui.step_indicator(i, total, f"Processing {item}"))
```

---

## Testing Commands

```bash
# Syntax check
python -m py_compile script.py

# Run with UI library
python script.py --help

# Test without UI library (rename/move the package temporarily)
mv /path/to/claude_terminal_ui /path/to/claude_terminal_ui.bak
python script.py --help
mv /path/to/claude_terminal_ui.bak /path/to/claude_terminal_ui

# Test no color mode
NO_COLOR=1 python script.py --help

# Test redirected output
python script.py --help > output.txt
cat output.txt
```

---

## Common Mistakes to Avoid

### ❌ DON'T
```python
# Don't mix old and new styles
print("="*70)
ui.header("TITLE")
print("="*70)

# Don't use raw Unicode symbols
print("✓ Success")  # Will fail on Windows cp1252

# Don't hardcode widths inconsistently
print("="*50)  # Different from standard 70
```

### ✅ DO
```python
# Use UI components consistently
print(ui.header("TITLE"))

# Let UI handle symbols
ui.print_success("Success")  # Automatic symbol selection

# Use standard widths
print(ui.header("TITLE"))  # Always 70 chars
```

---

## Additional Components

### Tables (if needed)
```python
ui.print_key_value({
    "Key 1": "Value 1",
    "Key 2": "Value 2"
})
```

### Progress bars (if needed)
```python
for i in range(100):
    print(f"\r{ui.progress_bar(i, 100)}", end="", flush=True)
```

### Spinners (if needed)
```python
with ui.spinner("Loading"):
    time.sleep(2)
```

---

## Fallback Testing

To ensure fallback works, temporarily disable the UI import:

```python
# Add to test file
UI_AVAILABLE = False  # Force fallback mode

# Or test with import error simulation
import sys
sys.modules['claude_terminal_ui'] = None
```

---

## Documentation Updates

After migration, update:
1. Migration report (CHECKPOINT_MIGRATION_REPORT.md style)
2. This quick reference (if new patterns found)
3. Main README (list migrated scripts)
4. Session protocol (if behavior changed)

---

## Success Criteria

✅ Script runs without errors
✅ All command-line arguments work
✅ Colors appear in terminal
✅ Fallback mode works
✅ NO_COLOR respected
✅ Redirected output works
✅ Functionality unchanged

---

**Last Updated:** 2025-12-30
**Based on:** checkpoint.py pilot migration
**Next Scripts:** save-session.py, resume-session.py, context-monitor.py
