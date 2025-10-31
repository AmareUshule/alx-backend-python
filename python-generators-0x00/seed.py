# seed.py
import psycopg2
import csv
import uuid

# --- Config ---
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "password"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
TABLE_NAME = "user_data"
# ---------------

def connect_db():
    """Connect to PostgreSQL server and return connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS,
            host=DB_HOST, port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None

def create_table(conn):
    """Create table if it does not exist."""
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """)
        conn.commit()
    print("Table user_data created successfully")

def insert_data(conn, csv_path):
    """Insert data from CSV into table if not exists."""
    with conn.cursor() as cur, open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        first = next(reader)
        if any(h.lower() in ("user_id", "user", "id") for h in first):
            pass
        else:
            reader = (row for row in [first] + list(reader))

        for row in reader:
            if len(row) < 4:
                continue
            user_id = row[0] if row[0] else str(uuid.uuid4())
            name, email, age = row[1], row[2], float(row[3])
            cur.execute(f"SELECT 1 FROM {TABLE_NAME} WHERE user_id = %s", (user_id,))
            if not cur.fetchone():
                cur.execute(
                    f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        conn.commit()
    print("Data inserted successfully")
