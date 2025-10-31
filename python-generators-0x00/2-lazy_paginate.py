# 2-lazy_paginate.py
"""
Implements lazy pagination using a generator.

Functions:
- paginate_users(page_size, offset): fetches one page from user_data.
- lazy_pagination(page_size): yields each page lazily.
"""

import psycopg2
from decimal import Decimal

# Database config (match your seed.py)
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "Mamare@2025@"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"


def _normalize_age(val):
    """Convert numeric to int or float cleanly."""
    if isinstance(val, Decimal):
        if val == val.to_integral_value():
            return int(val)
        return float(val)
    try:
        f = float(val)
        return int(f) if f.is_integer() else f
    except Exception:
        return val


def paginate_users(page_size, offset):
    """Fetch one page of results from user_data using LIMIT/OFFSET."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
    )
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert to list of dicts
    users = []
    for r in rows:
        users.append({
            "user_id": str(r[0]),
            "name": r[1],
            "email": r[2],
            "age": _normalize_age(r[3])
        })
    return users


def lazy_pagination(page_size):
    """Generator that lazily loads pages of users using one loop."""
    offset = 0
    while True:  # only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

