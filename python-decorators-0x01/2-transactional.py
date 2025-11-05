#!/usr/bin/python3
import sqlite3
import functools

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

def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper_transaction(*args, **kwargs):
        conn = args[0]  # Connection is passed from with_db_connection
        try:
            result = func(*args, **kwargs)
            conn.commit()
            print("[LOG] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[LOG] Transaction rolled back due to error: {e}")
            raise
    return wrapper_transaction

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update a user's email with automatic transaction handling."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    print(f"Email for user {user_id} updated to {new_email}")

# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

