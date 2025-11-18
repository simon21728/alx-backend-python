# Python Generators Project

## Overview
This project demonstrates how to use Python generators to stream rows from a MySQL database instead of loading all data into memory.

## Files
- `seed.py` – contains all database setup functions, data insertion, and the generator function.
- `user_data.csv` – sample dataset used to populate the `user_data` table.

## Functions
- `connect_db()` – Connects to the MySQL server.
- `create_database(connection)` – Creates `ALX_prodev` if it does not exist.
- `connect_to_prodev()` – Connects to the `ALX_prodev` database.
- `create_table(connection)` – Creates the `user_data` table with required fields.
- `insert_data(connection, csv_file)` – Inserts data from CSV if it does not exist.
- `stream_user_data(connection)` – Generator function to stream rows one by one.

## Usage
```python
import seed

conn = seed.connect_db()
seed.create_database(conn)
conn.close()

conn = seed.connect_to_prodev()
seed.create_table(conn)
seed.insert_data(conn, 'user_data.csv')

for row in seed.stream_user_data(conn):
    print(row)
