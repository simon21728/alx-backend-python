#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    """
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data;")

        # Yield rows one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
