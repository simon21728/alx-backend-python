import sqlite3
import functools

# --- Reuse from previous task ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('my_database.db')  # replace with your DB path
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# --- Transactional decorator ---
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # commit if everything went well
            return result
        except Exception as e:
            conn.rollback()  # rollback if any error occurs
            raise e  # re-raise the exception
    return wrapper

# --- Example function ---
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# --- Usage ---
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User email updated successfully.")
