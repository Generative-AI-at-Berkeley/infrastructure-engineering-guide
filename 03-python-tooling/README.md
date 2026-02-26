# Python Tooling (uv, ruff, ty)

**The Problem**
Python tooling used to be slow, inconsistent, and spread across too many tools. One person runs `pip install`, another uses `poetry`, CI runs something else, and linting is a mix of flake8, black, isort, and mypy. That means slow feedback and inconsistent results.

> Imagine you're Michael and all you want is a pack of Mevius coffee-flavored Japanese cigarettes. You ask for cigs but theres like 200m different types of cigs out there. But worst of all, every time you ask your friends, one comes back with Newports, another hands you some weird self-rolled pack of cigs he got off a seller on Ebay whose location literally says "somewhere in the amazon rainforest", and another says, "a cig is a cig." 
>
> Now, Michael decides to do it properly. He uses `uv` like the official importer—making sure every cigarette is exactly the Mevius coffee flavor he wants and none of that rep stuff sneaks in (dependency management and locking). He uses `ruff` to make sure the packaging isn't ripped, there's no broken filters, and all the warnings are in place (linting and formatting). Finally, `ty` is like the customs agent, scanning each pack to verify it's real, not messed with, and allowed through (type checking). So now, michael can smoke his mevius cigs in peace without worrying that he might be in peace indefinitely. 

**The Solution**
Use `uv` for dependency management, `ruff` for linting and formatting, and `ty` for type checking. These are fast, deterministic, and designed for CI. They are all Rust-based, which means they are fast enough to run on every commit.

**Real Code**
Here is a CI workflow snippet that enforces the full Python gate. Every non-obvious line is annotated.

```yaml
name: python-checks
on:
  pull_request:
    paths:
      - "backend/**"
      - "pyproject.toml"
      - "uv.lock"

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v3 # Installs uv fast, no pip bootstrap.
        with:
          version: "0.4.26"

      - name: Sync deps
        run: uv sync --locked # Fails if lockfile and pyproject drift.

      - name: Lint
        run: uv run ruff check . # Replaces flake8, isort, and a bunch of plugins.

      - name: Format
        run: uv run ruff format --check . # Replaces black, but much faster.

      - name: Typecheck
        run: uv run ty check # Fast type checking with good defaults.
```

**Key Lessons**
- `uv sync --locked` is your safety bar. If the lockfile is stale, CI fails.
- `uv run` makes the environment deterministic. No global installs, no surprise versions.
- `ruff` consolidates linting and formatting, so you enforce one tool, not five.
- Rust-based tooling wins because speed means you actually run it every time.

**How This Applies Elsewhere**
If your team uses Poetry, pip-tools, Black, Flake8, or Mypy, the pattern is identical: one lockfile, one lint gate, one typecheck gate. The tool names will change, the discipline stays.
