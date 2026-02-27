# Hands-On App (Tiny Postgres + Migrations)

This is a tiny, beginner-friendly app you can run locally. It exists so you can practice real production basics without any complexity.

You will:
- Start a real Postgres database
- Apply a migration to create a table
- Add a column with a second migration
- Insert and read data with Python
- Practice type checking with TypedDict + dataclass models

No cloud. No deployment. Just the fundamentals.

## What Is In This Folder
- `docker-compose.yml` starts Postgres
- `mise.toml` pins tools and provides `install`, `migrate`, `dev` tasks
- `migrations/` holds numbered SQL migrations
- `app/migrate.py` applies migrations in order
- `app/demo.py` inserts and reads data
- `app/types_practice.py` shows schema -> row type -> model flow
- `prisma/schema.prisma` maps Prisma models to the same `students` table
- `app/prisma_demo.mjs` writes/reads via Prisma client
- `PRISMA-README.md` explains Prisma details and patterns

## Getting Started

### 1) Start Postgres
From this folder:

```bash
cd /Users/yanjiezheng/Documents/BK/swe-practices-lesson/hands-on
docker compose up -d
```

If `docker compose` does not work, try `docker-compose up -d`.

### 2) Install mise + run one install command (Recommended)
`mise` is the task runner/orchestration layer. This gives one command path that feels like a real team environment.

If you do not have `mise`:

```bash
brew install mise
```

Then from this folder run:

```bash
mise install
mise run install
```

What `mise run install` does:
- Creates Python venv and installs `requirements.txt`
- Installs Node packages used by Prisma (`prisma`, `@prisma/client`)

### 3) Optional tooling sanity check (ruff + ty)
`uv` is a fast Python package manager. `ruff` is linting + formatting. `ty` is type checking.

If you have Homebrew (Mac):

```bash
brew install uv
```

Otherwise:

```bash
python -m pip install --user uv
```

Install the tools:

```bash
uv tool install ruff
uv tool install ty
```

Quick sanity check:

```bash
uv --version
ruff --version
ty --version
```

### 4) Run The First Migration
This creates the `students` table.

```bash
mise run migrate
```

`mise run migrate` runs SQL migrations first, then refreshes Prisma against the same schema (`db pull` + `generate`).

(Optional) Verify the table exists:

```bash
docker compose exec postgres psql -U app -d app -c "\dt"
```

### 5) Make A Schema Change
Create a new migration file called `migrations/002_add_email.sql` with this content:

```sql
ALTER TABLE students ADD COLUMN email TEXT;
```

The number at the start of the filename matters because migrations run in order.

### 6) Run Migrations Again

```bash
mise run migrate
```

### 7) Insert And Read Data
Now that the `email` column exists, run the demo script:

```bash
uv run python app/demo.py
```

You should see a new row printed.

### 8) Type Checking + Models Practice
This step shows why types and models matter:
- **Schema**: the Postgres table columns and constraints
- **TypedDict row type**: the expected shape of raw data in Python
- **dataclass model**: a clean in-memory representation your app uses
- **Type checking** (`ty`): catches mismatches before runtime

Run the practice script:

```bash
python app/types_practice.py
```

Type-check it:

```bash
ty check app/types_practice.py
```

Open `app/types_practice.py` and try these exercises:
1. Change `StudentRow.class_year` from `int` to `str` and run `ty check` again.
2. In `to_student`, remove the `email` key from the dict and see what breaks.
3. Uncomment the intentionally broken examples at the bottom and run `ty check`.

You should see clear type errors, which is exactly the point: types make schema drift obvious early.

### 9) Optional: Prisma Setup
Prisma is now pre-wired in this folder. You can run its demo directly:

```bash
npm run prisma:demo
```

Or run the full end-to-end flow:

```bash
mise run dev
```

`mise run dev`:
- starts/keeps Postgres running (`docker compose up -d postgres`)
- runs migrations
- runs Python demo
- runs Prisma demo

For details on Prisma model mapping and migration ownership, follow:

- `PRISMA-README.md`

## Shut Down

```bash
docker compose down
```

If you want to delete all data and start over:

```bash
docker compose down -v
```

## What You Just Learned
- How to run real dependencies locally (Postgres)
- How migrations apply schema changes safely and in order
- Why code depends on the database schema, not the other way around
- How schema, row types, and models fit together
- Why type checking catches bugs before runtime

That is the same flow you will see on real teams. The tools get bigger, but the idea stays the same.
