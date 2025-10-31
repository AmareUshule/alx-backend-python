# 1-batch_processing.py
"""
Batch processing using a generator.

Provides:
- stream_users_in_batches(batch_size): yields lists (batches) of user dicts
- batch_processing(batch_size): prints users with age > 25
"""

import psycopg2
from decimal import Decimal

# DB config (match your seed.py values)
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "Mamare@2025@"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
TABLE_NAME = "user_data"


def _normalize_age(val):
    """
    Convert DB numeric/Decimal to int if whole number, otherwise float.
    """
    if isinstance(val, Decimal):
        if val == val.to_integral_value():
            return int(val)
        return float(val)
    try:
        # fallback for other numeric types
        f = float(val)
        if f.is_integer():
            return int(f)
        return f
    except Exception:
        return val


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users (each batch is a list of dicts).
    Uses fetchmany(batch_size) to avoid loading entire table into memory.

    Constraint: only one loop here (while True with fetchmany).
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        cur = conn.cursor()
        cur.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME}")

        # single loop to fetch batches
        while True:
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            batch = []
            for r in rows:
                batch.append({
                    "user_id": str(r[0]),
                    "name": r[1],
                    "email": r[2],
                    "age": _normalize_age(r[3])
                })
            yield batch

        cur.close()
    except Exception as e:
        # yield nothing further if error occurs; print simple error for debugging
        print(f"Error in stream_users_in_batches: {e}")
    finally:
        if conn:
            conn.close()


def batch_processing(batch_size):
    """
    Process each batch produced by stream_users_in_batches and print users over age 25.

    Uses up to 2 loops:
      - loop over batches (in this function)
      - loop over users in each batch to filter and print
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                if user["age"] > 25:
                    print(user)
            except Exception:
                # if age is malformed for some row, skip it silently
                continue

