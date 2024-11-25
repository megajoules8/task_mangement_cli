# db_connection.py
import sqlite3

def connect_to_db():
    try:
        print("Connecting to the database...")
        conn = sqlite3.connect('task_manager.db')  # SQLite database file
        print("Connection object created")
        cursor = conn.cursor()
        print("Cursor object created")
        print("Connection successful")
        return conn, cursor
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None, None
