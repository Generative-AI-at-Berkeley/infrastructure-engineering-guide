# Hands-On App (Tiny Postgres + Migrations)

This is a tiny, beginner-friendly app you can run locally. It exists so you can practice real production basics without any complexity.

You will:
- Start a real Postgres database
- Apply a migration to create a table
- Add a column with a second migration
- Insert and read data with Python

No cloud. No deployment. Just the fundamentals.

## What Is In This Folder
- `docker-compose.yml` starts Postgres
- `migrations/` holds numbered SQL migrations
- `app/migrate.py` applies migrations in order
- `app/demo.py` inserts and reads data

## Getting Started

### 1) Start Postgres
From this folder:

```bash
cd /Users/yanjiezheng/Documents/BK/swe-practices-lesson/hands-on
docker compose up -d
```

If `docker compose` does not work, try `docker-compose up -d`.

### 2) Install uv + ruff + ty (Recommended)
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

### 3) Set Up Python
Create a virtual environment and install the one dependency:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4) Run The First Migration
This creates the `students` table.

```bash
python app/migrate.py
```

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
python app/migrate.py
```

### 7) Insert And Read Data
Now that the `email` column exists, run the demo script:

```bash
python app/demo.py
```

You should see a new row printed.

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

That is the same flow you will see on real teams. The tools get bigger, but the idea stays the same.
