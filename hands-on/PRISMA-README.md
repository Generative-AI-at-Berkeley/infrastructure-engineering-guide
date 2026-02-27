# Prisma In Hands-On (Same Postgres, No Container Tear-Down)

This folder now includes a ready Prisma setup that points to the same Postgres used by the Python scripts.

## What Is Already Wired
- `package.json` has Prisma dependencies and scripts.
- `prisma/schema.prisma` maps to the existing `students` SQL table.
- `mise.toml` has:
  - `mise run install`
  - `mise run migrate`
  - `mise run dev`

Default DB URL for both Python and Prisma:

```txt
postgresql://app:app@localhost:5432/app?schema=public
```

This builds on your existing running container and does not require `docker compose down`.

## Command Flow
From `hands-on/`:

```bash
mise install
mise run install
mise run migrate
mise run dev
```

What each command does:
- `mise run install`
  - `uv venv`
  - installs Python deps from `requirements.txt`
  - `npm install` for Prisma packages
- `mise run migrate`
  - runs SQL migrations (`uv run python app/migrate.py`)
  - introspects DB (`npm run prisma:db:pull`)
  - regenerates Prisma client (`npm run prisma:generate`)
- `mise run dev`
  - keeps Postgres up with `docker compose up -d postgres`
  - runs `mise run migrate`
  - runs Python demo and Prisma demo

## Why This Pattern
- SQL migrations remain source-of-truth for schema changes in this lab.
- Prisma is used for typed query ergonomics and model mapping.
- `db pull` keeps Prisma schema aligned to live DB.

This is a safe teaching pattern for schema + type alignment without mixing migration ownership.

## Prisma Model Mapping
Current model:

```prisma
model Student {
  id        Int      @id @default(autoincrement())
  name      String
  classYear Int      @map("class_year")
  email     String?
  createdAt DateTime @default(now()) @map("created_at")

  @@map("students")
}
```

`@map` and `@@map` bridge Python/SQL naming and app-level naming.

## Optional: If You Want Prisma To Own Migrations
Not recommended in this same lab unless you stop using SQL files.

If you do want to experiment anyway:

```bash
npm run prisma:migrate:dev -- --name init_students
```

Use this in a separate sandbox branch or folder to avoid conflicting migration histories.
