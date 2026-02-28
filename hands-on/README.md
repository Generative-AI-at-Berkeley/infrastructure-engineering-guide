# Hands-On: Tiny Postgres + Migrations + Prisma

This is a beginner-friendly lab. You will run a real Postgres database, apply migrations, and read/write data with both Python and Prisma.

## What You Will Build
- A local Postgres database in Docker
- A `students` table created by migrations
- A tiny Python script that inserts and reads data
- A Prisma client that reads/writes the same table

## Install Everything (With Download Links)
If you already have these, skip this section.

### 1) Docker
Mac (Apple Silicon):
- Install [OrbStack](https://orbstack.dev/download)

Mac (Intel), Windows, Linux:
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Verify:

```bash
docker ps
```

### 2) Node.js (for Prisma)
Install Node.js LTS:
- [Node.js Downloads](https://nodejs.org/en/download)

Verify:

```bash
node -v
npm -v
```

### 3) Python 3.11+
Install Python:
- [Python Downloads](https://www.python.org/downloads/)

Verify:

```bash
python --version
```

### 4) uv + ruff + ty
`uv` is a fast Python package manager. `ruff` is linting + formatting. `ty` is type checking.

Mac (Homebrew):

```bash
brew install uv
```

Anywhere else:

```bash
python -m pip install --user uv
```

Install ruff and ty:

```bash
uv tool install ruff
uv tool install ty
```

Verify:

```bash
uv --version
ruff --version
ty --version
```

## Run The Lab

### 1) Start Postgres
From this folder:

```bash
cd /Users/yanjiezheng/Documents/BK/swe-practices-lesson/hands-on
docker compose up -d
```

If `docker compose` does not work, try `docker-compose up -d`.

### 2) Install Dependencies
Python:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Node (for Prisma):

```bash
npm install
```

### 3) Run The First Migration
This creates the `students` table.

```bash
python app/migrate.py
```

Update Prisma to match the DB:

```bash
npm run prisma:db:pull
npm run prisma:generate
```

(Optional) Verify the table exists:

```bash
docker compose exec postgres psql -U app -d app -c "\dt"
```

### 4) Make A Schema Change
Create a new migration file called `migrations/002_add_email.sql` with this content:

```sql
ALTER TABLE students ADD COLUMN email TEXT;
```

The number at the start of the filename matters because migrations run in order.

### 5) Run Migrations Again

```bash
python app/migrate.py
npm run prisma:db:pull
npm run prisma:generate
```

### 6) Insert And Read Data (Python)

```bash
python app/demo.py
```

You should see a new row printed.

### 7) Insert And Read Data (Prisma)

```bash
npm run prisma:demo
```

## Optional: Type Checking Practice

```bash
ty check app/types_practice.py
```

Open `app/types_practice.py` and try these exercises:
1. Change `StudentRow.class_year` from `int` to `str` and run `ty check` again.
2. In `to_student`, remove the `email` key from the dict and see what breaks.
3. Uncomment the intentionally broken examples at the bottom and run `ty check`.

## Optional: One-Command Tasks (mise)
If you want a team-style task runner, use:
- `hands-on/mise.toml`
- `mise run install`
- `mise run migrate`
- `mise run dev`

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
- How Prisma maps to a live schema

That is the same flow you will see on real teams. The tools get bigger, but the idea stays the same.
