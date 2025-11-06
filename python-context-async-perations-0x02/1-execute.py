"""Reusable query context manager"""

import sqlite3

class ExecuteQuery:
    """Custom context manager that executes a query and returns results"""
    
    def __init__(self, query, params=None, db_name="mydb.sqlite"):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open connection and execute the query"""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection"""
        if self.conn:
            self.conn.close()
        return False  # propagate exceptions


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        for row in results:
            print(row)

