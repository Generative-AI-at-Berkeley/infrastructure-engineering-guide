from dataclasses import dataclass
from typing import TypedDict

from db import get_conn


class StudentRow(TypedDict):
    id: int
    name: str
    class_year: int
    email: str | None


@dataclass(slots=True)
class Student:
    id: int
    name: str
    class_year: int
    email: str | None


def fetch_recent_student_rows(limit: int = 5) -> list[StudentRow]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, class_year, email
                FROM students
                ORDER BY id DESC
                LIMIT %s;
                """,
                (limit,),
            )
            rows = cur.fetchall()

    typed_rows: list[StudentRow] = []
    for row in rows:
        typed_rows.append(
            {
                "id": row[0],
                "name": row[1],
                "class_year": row[2],
                "email": row[3],
            }
        )
    return typed_rows


def to_student(row: StudentRow) -> Student:
    return Student(
        id=row["id"],
        name=row["name"],
        class_year=row["class_year"],
        email=row["email"],
    )


def email_domain(student: Student) -> str:
    if student.email is None:
        return "no-email"
    return student.email.split("@")[-1]


def main() -> None:
    rows = fetch_recent_student_rows()
    students = [to_student(row) for row in rows]

    print("Students (typed model objects):")
    for student in students:
        print(
            f"id={student.id}, name={student.name}, "
            f"class_year={student.class_year}, domain={email_domain(student)}"
        )


if __name__ == "__main__":
    main()


# ---------------------------
# Practice: uncomment one block at a time and run:
#   ty check app/types_practice.py
# ---------------------------

# Example 1: wrong field type for schema row shape.
# bad_row: StudentRow = {
#     "id": "1",  # should be int
#     "name": "Ada",
#     "class_year": 2,
#     "email": "ada@example.com",
# }

# Example 2: None handling bug.
# def broken_email_domain(student: Student) -> str:
#     return student.email.split("@")[-1]  # student.email can be None
