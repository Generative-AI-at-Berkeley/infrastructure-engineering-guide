from pathlib import Path

from db import get_conn

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


def ensure_migrations_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )


def get_applied_ids(cur):
    cur.execute("SELECT id FROM schema_migrations;")
    return {row[0] for row in cur.fetchall()}


def main():
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not files:
        print("No migrations found.")
        return

    with get_conn() as conn:
        with conn.cursor() as cur:
            ensure_migrations_table(cur)
            applied = get_applied_ids(cur)

        for path in files:
            if path.name in applied:
                continue

            sql = path.read_text().strip()
            if not sql:
                continue

            print(f"Applying {path.name}...")
            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    cur.execute(
                        "INSERT INTO schema_migrations (id) VALUES (%s);",
                        (path.name,),
                    )
                conn.commit()
                applied.add(path.name)
            except Exception:
                conn.rollback()
                raise

    print("Done.")


if __name__ == "__main__":
    main()



# this is stack one, stack two needs to call stack one

def do_something():
    print("doing something")

# def do_something_else():
#     print("doing something else")

# def main():
#     do_something()
#     do_something_else()

