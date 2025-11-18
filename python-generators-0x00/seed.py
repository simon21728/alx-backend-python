#!/usr/bin/python3
import mysql.connector
import csv
import uuid

# -------------------------------
# Connect to MySQL server
# -------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# -------------------------------
# Create database if not exists
# -------------------------------
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

# -------------------------------
# Connect to ALX_prodev database
# -------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

# -------------------------------
# Create table user_data
# -------------------------------
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """)
        print("Table user_data created successfully")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

# -------------------------------
# Insert data from CSV
# -------------------------------
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if user_id exists
                cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (row['user_id'],))
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (row['user_id'], row['name'], row['email'], row['age'])
                    )
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

# -------------------------------
# Generator to stream rows one by one
# -------------------------------
def stream_user_data(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    finally:
        cursor.close()
