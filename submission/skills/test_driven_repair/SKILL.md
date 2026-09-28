
---
name: test_driven_repair
description: Find relevant tests, run narrow tests first, interpret failures, expand test scope after success, and iterate on code fixes using test feedback.
whenToUse: When writing or fixing code, when verifying a patch, or when iterating on a solution.
---

# Test-Driven Repair

## Finding Relevant Tests

1. **Search the issue text** for test names, error messages, or expected behavior
2. **Search the codebase** for test files related to the changed module:
   ```bash
   find . -path "*/tests/*" -name "*.py" | grep -i "module_name"
   grep -rn "def test.*feature" --include="*.py" tests/
   ```
3. **Look for pytest markers** or test class names that match the issue

## Run Narrow Tests First

Always start with the most targeted test:

```bash
# Single test method
python -m pytest tests/test_module.py::TestClass::test_method -x -q

# Single test class
python -m pytest tests/test_module.py::TestClass -x -q

# Single test file
python -m pytest tests/test_module.py -x -q
```

Use `-x` to stop at the first failure, `-q` for quiet output.

## Interpreting Failures

When a test fails:

- **RED** = test fails (implementation is wrong or test needs different input)
- **GREEN** = test passes (implementation is correct for this case)
- **Did the right test run?** — verify the test name matches what you expect

## Expanding Test Scope

After narrow tests pass:

```bash
# Run the full test file
python -m pytest tests/test_module.py -q

# Run related test files
python -m pytest tests/test_module.py tests/test_other.py -q

# Run the full suite (only if time permits)
python -m pytest tests/ -q
```

## Patching Strategy

1. **Make the minimal change** — fix the root cause, not symptoms
2. **Run the narrow failing test** — confirm it now passes
3. **Run the broader test file** — check for regressions
4. **Repeat** — if new failures, go back to step 1

## Important

- **Never modify test files** — the harness resets test files before verification
- **Put scratch scripts in `/tmp/`** — files in `/workspace` leak into your patch
- **Clean up before `submit_patch()`** — `git diff HEAD` captures everything in `/workspace`
