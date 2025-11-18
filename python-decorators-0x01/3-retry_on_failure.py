import time
import sqlite3
import functools

# --- Reuse from previous task ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')  # replace with your DB path
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# --- Retry decorator ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        raise  # re-raise the last exception
                    print(f"Attempt {attempt} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator

# --- Example function ---
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Usage ---
users = fetch_users_with_retry()
print(users)
