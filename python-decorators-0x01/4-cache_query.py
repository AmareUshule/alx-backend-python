#!/usr/bin/python3
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

def with_db_connection(func):
    """Decorator to automatically handle database connections."""
    @functools.wraps(func)
    def wrapper_with_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_connection

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper_cache_query(*args, **kwargs):
        # Determine the query string
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 1:  # First arg is conn
            query = args[1]
        else:
            raise ValueError("No SQL query provided to cache.")

        # Return cached result if exists
        if query in query_cache:
            print("[CACHE] Using cached result.")
            return query_cache[query]

        # Execute function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Query result cached.")
        return result

    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from the database with caching."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call uses cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)

