"""Class-based context manager for database connections"""

import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connection"""
    
    def __init__(self, db_name="mydb.sqlite"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
        # Returning False re-raises any exceptions that occurred inside the with block
        return False


# Example usage
if __name__ == "__main__":
    # Using the context manager to query the 'users' table
    with DatabaseConnection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            for row in results:
                print(row)
        except sqlite3.Error as e:
            print(f"Database error: {e}")

