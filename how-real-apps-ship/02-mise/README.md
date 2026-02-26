# mise

**The Problem**
Everyone has a slightly different toolchain. One person has Node 18, another has Node 20. Someone forgot to upgrade Python. CI uses a different version entirely. This is how you ship bugs that only happen on one machine.

**The Solution**
Use `mise` to pin tool versions and define shared tasks. It replaces the sprawl of `nvm`, `pyenv`, `asdf`, and ad-hoc README steps. You install once, and every developer gets the same versions and the same commands.

**Real Code**
Below is a real `mise.toml` pattern with version pinning and tasks. Every non-obvious line is annotated.

```toml
[tools]
node = "20.11.1" # Frontend build and tooling.
python = "3.11.7" # Backend runtime.
terraform = "1.6.6" # IaC tooling pinned for reproducible plans.

[env]
PYTHONUNBUFFERED = "1" # Make logs show up immediately.
DATABASE_URL = "postgres://app:app@localhost:5432/app" # Local dev default.

[tasks.install]
run = "uv sync --locked" # One command to sync Python deps from lockfile.

[tasks.dev]
run = "docker-compose up" # Local dependencies in containers.

[tasks.check]
run = "uv run ruff check . && uv run ruff format --check . && uv run ty check" # Single quality gate.

[tasks.test]
run = "uv run pytest" # Standardized test entry point.
```

**Key Lessons**
- Pin versions in one file so everyone uses the same toolchain.
- A task runner is not a nice-to-have. It is how you standardize commands across the team.
- `mise` removes most README setup drift. If it is in `mise.toml`, it is real.

**How This Applies Elsewhere**
If your team uses `asdf`, `nvm` plus `pyenv`, or a `Makefile` full of fragile commands, the idea is the same: a single source of truth for versions and tasks.
