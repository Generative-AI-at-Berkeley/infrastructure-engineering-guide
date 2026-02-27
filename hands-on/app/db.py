import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://app:app@localhost:5432/app")

LOG_PATH = "/Users/helluri/gen-ai-berk/infrastructure-engineering-guide/.cursor/debug-1b920d.log"


def _connection_url_for_psycopg(url: str) -> str:
    """Remove query parameters psycopg doesn't support (e.g. schema)."""
    parsed = urlparse(url)
    if not parsed.query:
        return url
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("schema", None)
    if not params:
        new_query = ""
    else:
        new_query = urlencode(
            [(k, v) for k, vals in params.items() for v in vals],
            doseq=True,
        )
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )


def get_conn():
    # #region agent log
    import json

    conn_url = _connection_url_for_psycopg(DATABASE_URL)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(
                json.dumps(
                    {
                        "sessionId": "1b920d",
                        "hypothesisId": "A",
                        "location": "db.py:get_conn",
                        "message": "DATABASE_URL and stripped URL",
                        "data": {
                            "raw_has_schema": "schema=" in (DATABASE_URL or ""),
                            "stripped": True,
                        },
                        "timestamp": __import__("time").time() * 1000,
                    }
                )
                + "\n"
            )
    except Exception:
        pass
    # #endregion
    return psycopg.connect(conn_url)
