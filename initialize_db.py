# initialize_db.py
import sqlite3

def initialize_db():
    try:
        print("Connecting to the database...")
        conn = sqlite3.connect('task_manager.db')  # SQLite database file
        cursor = conn.cursor()
        print("Connected to the database.")

        # Create users table if it doesn't exist
        print("Creating users table if it doesn't exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
        print("Users table created or already exists.")

        # Create tasks table if it doesn't exist
        print("Creating tasks table if it doesn't exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        conn.commit()
        print("Tasks table created or already exists.")

        # Add new column 'priority' to tasks table if it doesn't exist
        print("Adding 'priority' column to tasks table if it doesn't exist...")
        cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT")
        conn.commit()
        print("Priority column added to tasks table.")

        # Create task_assignments table if it doesn't exist
        print("Creating task_assignments table if it doesn't exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_assignments (
            task_id INTEGER,
            user_id INTEGER,
            PRIMARY KEY (task_id, user_id),
            FOREIGN KEY (task_id) REFERENCES tasks (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        conn.commit()
        print("Task_assignments table created or already exists.")

        # Close the database connection
        conn.close()
        print("Database initialization complete.")
    except sqlite3.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    initialize_db()