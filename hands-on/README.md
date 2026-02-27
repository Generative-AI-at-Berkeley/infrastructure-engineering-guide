# Hands-On: A Tiny App With Real Infrastructure Basics

This is a beginner-friendly, step-by-step walkthrough. You will:
- Start a real Postgres database with Docker
- Apply a migration to create a table
- Add a new column with a second migration
- Insert and read data with a tiny Python script

No cloud, no IaC, no fancy frameworks. Just the basics that every real app needs.

## Folder Layout
- `docker-compose.yml` starts Postgres
- `migrations/` holds numbered SQL migrations
- `app/migrate.py` applies migrations in order
- `app/demo.py` inserts and reads data

## Step 0: Prereqs
Install these once:
- Docker Desktop
- Python 3.10+ (3.11 is great)

## Step 1: Start Postgres
From this folder:

```bash
cd /Users/yanjiezheng/Documents/BK/swe-practices-lesson/hands-on
docker compose up -d
```

If `docker compose` does not work, try `docker-compose up -d`.

Give it a few seconds to boot the first time.

## Step 2: Set Up Python
Create a virtual environment and install the one dependency:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Step 3: Run The First Migration
This creates the `students` table.

```bash
python app/migrate.py
```

(Optional) Verify the table exists:

```bash
docker compose exec postgres psql -U app -d app -c "\dt"
```

## Step 4: Change The Schema (Add A Column)
Create a new migration file called `migrations/002_add_email.sql` with this content:

```sql
ALTER TABLE students ADD COLUMN email TEXT;
```

You can create it however you want (editor or copy/paste). The filename number matters because migrations run in order.

## Step 5: Run Migrations Again
This applies the new migration and adds the column.

```bash
python app/migrate.py
```

## Step 6: Insert And Read Data
Now that the `email` column exists, run the demo script:

```bash
python app/demo.py
```

You should see a new row printed.

## Step 7: Shut Down (When You're Done)

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

When you do this on a real team, the same patterns apply. The tools get bigger, but the idea stays the same.
