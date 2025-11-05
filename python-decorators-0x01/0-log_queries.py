
import sqlite3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        # Detect the SQL query argument
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]
        else:
            query = '<No query provided>'
        
        print(f"[LOG] Executing SQL query: {query}")
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

