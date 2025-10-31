# seed.py
import psycopg2
import csv
import uuid

# --- Config ---
DB_NAME = "alx_prodev"
DB_USER = "amare"
DB_PASS = "Mamare@2025@"
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
    """Insert data from CSV into table, generate UUID for each row."""
    with conn.cursor() as cur, open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the header row

        for row in reader:
            if len(row) < 3:  # only name, email, age
                continue
            user_id = str(uuid.uuid4())  # generate UUID
            name, email, age = row[0], row[1], float(row[2])
            cur.execute(f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age))
            print(f"Inserted {name} ({email}, {age})")  # debug print
        conn.commit()
    print("All data inserted successfully")


# --- Run script ---
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_table(conn)
        insert_data(conn, "user_data.csv")
        conn.close()
