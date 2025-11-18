import sqlite3

class ExecuteQuery:
    """Custom context manager that executes a query with parameters"""
    
    def __init__(self, query, params=None, db_path='my_database.db'):
        self.query = query
        self.params = params or ()
        self.db_path = db_path
        self.conn = None
        self.result = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close connection and handle rollback/commit
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
        return False  # propagate exception if any

# --- Usage ---
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as users_over_25:
    print(users_over_25)
