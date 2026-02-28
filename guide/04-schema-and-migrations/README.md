# Schema And Migrations

**The Problem**
Databases do not magically update when you change your code. If you deploy code that expects a new column before the migration runs, your app crashes in production. If you forget which change happened when, you cannot debug or roll back safely.

> When Yanjie slacks his coworkers, he lowkey always forgets to add context and it lowkey terrorizes some of his coworkers. 

>One day, he slacks his staff engineer 

>"yo i added the ai stuff into the pr", the response he gets is 

>"what? i have absolutely no clue what you just said. wtf is "the ai stuff" and what "pr"????"

> With migrations, he can automatically paste in context from what he wants to tell his staff engineer vs what he actually tells his staff engineer, and the staff engineer wont just glitch out irl from reading his message and will actually know what yanjie is saying and how to help him.

**The Solution**
Treat the schema as code and use numbered, versioned migration files. Migrations run before deploy so the database is always ahead of the code, never behind it.

**Real Code**
Below is a Prisma-flavored example that stays ORM-agnostic in concept. Every non-obvious line is annotated.

```prisma
// schema.prisma
model Order {
  id        String   @id @default(cuid())
  status    String   @default("PENDING")
  totalCents Int     @default(0)
  createdAt DateTime @default(now())
}
```

```text
prisma/migrations/20240217153000_add_total_cents/
  migration.sql
```

```sql
-- migration.sql
ALTER TABLE "Order" ADD COLUMN "totalCents" INTEGER NOT NULL DEFAULT 0;
```

```ts
// test/helpers/assertTestDB.ts
export function assertTestDB() {
  const url = process.env.DATABASE_URL || "";
  const expected = "postgres://app:app@localhost:5432/app_test";
  if (url !== expected) {
    throw new Error(
      `Refusing to run tests on non-test DB. Expected ${expected}, got ${url}`
    );
  }
}
```

**Key Lessons**
- Migrations are code. They are reviewed, versioned, and deployed just like application changes.
- Always run migrations before deploy. Code can handle extra columns, but it cannot handle missing ones.
- Numbered migration files create a reliable history. You can debug and roll back with confidence.
- `assertTestDB()` is a guardrail. It prevents "god forbid" tests from touching dev or prod data.

**How This Applies Elsewhere**
Prisma is one implementation. Django ORM, Alembic, Flyway, and Knex all follow the same principle: schema as code plus ordered migrations.
