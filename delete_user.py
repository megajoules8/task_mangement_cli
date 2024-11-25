# delete_user.py
import sqlite3

def delete_user():
    username = input("Enter the username of the user to delete: ").strip()
    
    try:
        conn = sqlite3.connect('task_manager.db')  # SQLite database file
        cursor = conn.cursor()
        print("Connected to the database.")
        
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"User '{username}' deleted successfully.")
        
        # Close the database connection
        conn.close()
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    delete_user()