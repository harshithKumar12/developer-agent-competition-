---
name: debugging
description: Debug test failures and code issues through systematic error classification, stack-trace analysis, root-cause isolation, targeted testing, and regression checking.
whenToUse: When a test fails, when a command returns an error, or when you need to understand why your code change did not produce the expected result.
---

# Debugging Methodology

## Error Classification

When a test or command fails, classify the error:

1. **Logic error** — The code runs but produces wrong results
2. **Import/syntax error** — Python can't import or parse the code
3. **Assertion error** — Code runs but output doesn't match expectations
4. **Test invocation error** — Wrong test path, wrong arguments
5. **Missing dependency** — A related code path also needs changes
6. **Edge case missed** — Fix works for the main case but not boundary cases

## Stack-Trace Analysis

1. Read the **full error message** (scroll down if truncated)
2. Identify the **error type** (AssertionError, ImportError, etc.)
3. Find the **traceback** — the deepest frame in your code is the likely root cause
4. Note the **file and line number** in the traceback
5. Look for the **assertion message** or **error message** text

## Root-Cause Isolation

For each failing test:

1. **Read the test** — understand exactly what it expects
2. **Read the implementation** — understand what it actually does
3. **Compare** — find where the two diverge
4. **Fix the implementation, not the test** — test files are reset before verification

## Targeted Testing

After a fix:

```bash
# Run the single failing test first
python -m pytest tests/test_file.py::TestClass::test_method -x -q

# Then the file
python -m pytest tests/test_file.py -x -q

# Then the directory (optional, time permitting)
python -m pytest tests/ -x -q
```

## Regression Checking

After fixing one issue:

1. **Re-run the previously passing tests** to ensure no regression
2. **Check for related code** that might have the same bug (e.g., similar parsing logic)
3. **Look for edge cases** — empty inputs, None values, type boundaries

## Budget Discipline

If a test fails **three times** with the same error:

1. **Stop executing** — switch to diagnosis
2. **Re-read** the test and implementation carefully
3. **Check the test expectations** — are you testing the right thing?
4. **Consider whether the failing test is actually testing the feature** you're implementing

Do NOT repeatedly run identical commands without learning something new.
