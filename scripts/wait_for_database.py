import os
import sys
import time

import psycopg2

from app.db_config import build_database_url

DATABASE_URL = build_database_url("DB")
MAX_ATTEMPTS = int(os.getenv("DATABASE_WAIT_ATTEMPTS", "30"))
SLEEP_SECONDS = float(os.getenv("DATABASE_WAIT_SECONDS", "2"))

for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        connection.close()
        print("Database is ready to accept connections.", flush=True)
        sys.exit(0)
    except psycopg2.OperationalError as exc:
        print(
            f"Database is not ready yet "
            f"(attempt {attempt}/{MAX_ATTEMPTS}): {exc}",
            flush=True,
        )
        if attempt == MAX_ATTEMPTS:
            print("Database readiness check failed.", flush=True)
            sys.exit(1)
        time.sleep(SLEEP_SECONDS)
