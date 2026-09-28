---

name: repo_navigation
description: Navigate code repositories efficiently using semantic search, code graphs, symbol resolution, and targeted file reads. Avoid reading entire repositories; progressively narrow the search space.
whenToUse: When you need to find code, understand repository structure, locate definitions or callers of symbols, or trace dependencies. Use before making any edits.
---

# Repository Navigation

## Principle: Progressive Narrowing

Never read an entire repository. Narrow the search space step by step:

1. **Survey** — `find . -maxdepth 3` + `cat README.md | head -30` to understand structure
2. **Semantic search** — `search_similar_code("SymbolName")` to find relevant symbols
3. **Graph traversal** — `get_code_neighbors(node)` to find callers/callees/imports
4. **Targeted read** — `read_file` only after narrowing to specific files/regions

## Code-Intelligence Tools

When pre-built graph data exists for the repository:

- `search_similar_code(query)`: Pass a **symbol name** (class, function, module), e.g., `"FastAPI.get"`. NOT a natural-language sentence. Returns top-k nodes with code snippets and similarity scores.
- `get_code_neighbors(node)`: Use results from `search_similar_code`. Filter by `edge_type`:
  - `"CALLS"` — what this function calls
  - `"CALLED_BY"` / incoming — what calls this function
  - `"DEFINED_IN"` — which file/module defines this symbol
  - `"IMPORTS"` — what this module imports
- `get_code_subgraph(nodes)`: Pass 2–10 related symbols to see their induced subgraph.

## Without Code-Intelligence Tools

If the graph tools return empty or error (no pre-built data for this repo):

```bash
# Find definitions
grep -rn "def function_name\|class ClassName" --include="*.py" .

# Find references
grep -rn "symbol_name" --include="*.py" .

# Find test files
find . -path "*/tests/*" -name "*.py" | head -20

# Find specific file
find . -name "*.py" -not -path "./.git/*" | head -50
```

## Key Commands

```bash
# Top-level structure (avoid .git, __pycache__)
find . -maxdepth 3 -not -path './.git/*' -not -path './__pycache__/*' | head -60

# Recent git history
git log --oneline -10

# File listing for a package
ls package/

# Test file discovery
find . -path "*/tests/*" -name "test_*.py" -o -path "*/tests/*" -name "*_test.py" | head -20
```

## Repository Orientation Checklist

- [ ] Identify the language/framework (Python, FastAPI, etc.)
- [ ] Identify the entry point and package structure
- [ ] Identify test framework (pytest) and test directory layout
- [ ] Identify how changes are tested (test command, test paths)
- [ ] Check for a `conftest.py` that might affect test collection
