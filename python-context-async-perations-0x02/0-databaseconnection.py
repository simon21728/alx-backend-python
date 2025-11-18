import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connection"""
    
    def __init__(self, db_path='my_database.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure the connection is closed
        if self.conn:
            if exc_type is None:
                self.conn.commit()  # commit changes if no exception
            else:
                self.conn.rollback()  # rollback on exception
            self.conn.close()
        # Returning False propagates exception if any occurred
        return False

# --- Usage ---
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
