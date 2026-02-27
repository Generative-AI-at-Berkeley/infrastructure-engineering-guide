import os

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://app:app@localhost:5432/app")


def get_conn():
    return psycopg.connect(DATABASE_URL)
