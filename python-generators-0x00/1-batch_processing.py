#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows from user_data table in batches.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        offset = 0
        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            rows = cursor.fetchall()
            if not rows:
                break
            for row in rows:
                yield row  # <-- use yield, not return
            offset += batch_size

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    """
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            print(user)
