# 0-stream_users.py
import psycopg2
import uuid

# Database configuration
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "Mamare@2025@"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
TABLE_NAME = "user_data"

def stream_users():
    """Generator that fetches users one by one from the database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS,
            host=DB_HOST, port=DB_PORT
        )
        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME}")
            for row in cur.fetchall():  # only 1 loop
                yield {
                    "user_id": str(row[0]),
                    "name": row[1],
                    "email": row[2],
                    "age": float(row[3])
                }
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

