import sqlite3
import functools
from datetime import datetime  # Added to log timestamps

def log_queries(func):
    """Decorator to log SQL queries with timestamp before executing them."""
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        # Detect the SQL query argument
        query = kwargs.get('query', args[0] if args else '<No query provided>')
        
        # Log the query with timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] [LOG] Executing SQL query: {query}")
        
        # Execute the actual function
        return func(*args, **kwargs)
    
    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    """Fetch all users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
