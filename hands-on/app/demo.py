from db import get_conn


def main():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (name, class_year, email) VALUES (%s, %s, %s) RETURNING id;",
                ("Ada Lovelace", 2, "ada@example.com"),
            )
            new_id = cur.fetchone()[0]
            conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, class_year, email FROM students ORDER BY id DESC LIMIT 5;"
            )
            rows = cur.fetchall()

    print(f"Inserted student id={new_id}")
    print("Recent rows:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
