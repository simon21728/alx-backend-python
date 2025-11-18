import time
import sqlite3
import functools

# --- Reuse from previous tasks ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')  # replace with your DB path
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# --- Cache dictionary ---
query_cache = {}

# --- Cache decorator ---
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Expecting 'query' to be passed as keyword argument
        query = kwargs.get('query')
        if query is None:
            raise ValueError("The 'query' keyword argument is required for caching.")

        if query in query_cache:
            print("Returning cached result...")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Caching result...")
        return result
    return wrapper

# --- Example function ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# --- Usage ---
# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
