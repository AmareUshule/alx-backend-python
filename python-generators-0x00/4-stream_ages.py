# 4-stream_ages.py
"""
Memory-efficient aggregation using generators.

Functions:
- stream_user_ages(): generator that yields ages one by one from user_data
- calculate_average_age(): computes the average age using the generator
"""

import psycopg2
from decimal import Decimal

# Database config (match your seed.py)
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "Mamare@2025@"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
TABLE_NAME = "user_data"


def _normalize_age(val):
    """Convert numeric/Decimal to int or float cleanly."""
    if isinstance(val, Decimal):
        if val == val.to_integral_value():
            return int(val)
        return float(val)
    try:
        f = float(val)
        return int(f) if f.is_integer() else f
    except Exception:
        return val


def stream_user_ages():
    """Generator that yields user ages one by one."""
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
        cur.execute(f"SELECT age FROM {TABLE_NAME}")
        for row in cur.fetchall():  # single loop to stream ages
            yield _normalize_age(row[0])
        cur.close()
    except Exception as e:
        print(f"Error in stream_user_ages: {e}")
    finally:
        if conn:
            conn.close()


def calculate_average_age():
    """Calculate average age using the generator, without loading all data at once."""
    total = 0
    count = 0
    for age in stream_user_ages():  # loop over generator
        total += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average = total / count
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()

