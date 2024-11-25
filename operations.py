import sqlite3
from decorators import auth_required, log_action
import os
import sys
import bcrypt
# Add the current directory to the system path
sys.path.append(os.path.dirname(__file__))
def login(cursor):
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            print("Login successful!")
            return user
        else:
            print("Invalid username or password.")
            return None
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return None

def register(cursor, conn):
    username = input("Enter a new username: ").strip()
    password = input("Enter a new password: ").strip()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

def logout():
    print("Logged out successfully.")


@auth_required
@log_action("Viewing tasks")
def view_tasks(cursor, user, current_user=None):
    try:
        user_id = user[0]  # Assuming the user ID is the first element in the user tuple
        cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, GROUP_CONCAT(users.username, ', ') as assignees
        FROM tasks
        JOIN task_assignments ON tasks.id = task_assignments.task_id
        JOIN users ON task_assignments.user_id = users.id
        WHERE tasks.id IN (
            SELECT task_id FROM task_assignments WHERE user_id = ?
        )
        GROUP BY tasks.id
        """, (user_id,))
        tasks = cursor.fetchall()
        if tasks:
            for task in tasks:
                print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}, Priority: {task[4]}, Due Date: {task[5]}, Assigned to: {task[6]}")
        else:
            print("No tasks found.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Viewing all tasks")
def view_all_tasks(cursor, current_user=None):
    try:
        cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, GROUP_CONCAT(users.username, ', ') as assignees
        FROM tasks
        JOIN task_assignments ON tasks.id = task_assignments.task_id
        JOIN users ON task_assignments.user_id = users.id
        GROUP BY tasks.id
        """)
        tasks = cursor.fetchall()
        if tasks:
            for task in tasks:
                print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}, Priority: {task[4]}, Due Date: {task[5]}, Assigned to: {task[6]}")
        else:
            print("No tasks found.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Creating task")
def create_task(cursor, conn, user_id, current_user=None):
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    status = input("Enter task status: ").strip()
    
    # Loop until a valid priority is entered
    while True:
        priority = input("Enter task priority (High, Medium, Low): ").strip().capitalize()
        if priority in ['High', 'Medium', 'Low']:
            break
        print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")
    
    due_date = input("Enter task due date (YYYY-MM-DD): ").strip()
    category = input("Enter task category: ").strip()
    
    try:
        cursor.execute("INSERT INTO tasks (title, description, status, priority, due_date, category, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, description, status, priority, due_date, category, user_id))
        task_id = cursor.lastrowid
        conn.commit()
        print("Task created successfully.")
        
        # Assign the task to the creator by default
        cursor.execute("INSERT INTO task_assignments (task_id, user_id) VALUES (?, ?)", (task_id, user_id))
        conn.commit()
        print("Task assigned to the creator.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Updating task")
def update_task(cursor, conn, user_id, current_user=None):
    # Display the user's tasks
    try:
        cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, GROUP_CONCAT(users.username, ', ') as assignees
        FROM tasks
        JOIN task_assignments ON tasks.id = task_assignments.task_id
        JOIN users ON task_assignments.user_id = users.id
        WHERE task_assignments.user_id = ?
        GROUP BY tasks.id
        """, (user_id,))
        tasks = cursor.fetchall()
        if tasks:
            print("Your tasks:")
            for task in tasks:
                print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}, Priority: {task[4]}, Due Date: {task[5]}, Assigned to: {task[6]}")
        else:
            print("No tasks found.")
            return
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return

    # Ask for the task ID to update
    task_id = input("Enter task ID to update: ").strip()

    # Fetch the current task details
    try:
        cursor.execute("SELECT title, description, status, priority, due_date FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        task = cursor.fetchone()
        if not task:
            print("Task not found.")
            return
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return

    # Ask for new task details, allowing the user to leave fields empty to keep them unchanged
    new_title = input(f"Enter new task title (leave empty to keep '{task[0]}'): ").strip()
    new_description = input(f"Enter new task description (leave empty to keep '{task[1]}'): ").strip()
    new_status = input(f"Enter new task status (leave empty to keep '{task[2]}'): ").strip()
    new_priority = input(f"Enter new task priority (leave empty to keep '{task[3]}'): ").strip()
    new_due_date = input(f"Enter new task due date (leave empty to keep '{task[4]}'): ").strip()

    if new_priority and new_priority not in ['High', 'Medium', 'Low']:
        print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")
        return

    # Use the current values if the user leaves the input empty
    new_title = new_title if new_title else task[0]
    new_description = new_description if new_description else task[1]
    new_status = new_status if new_status else task[2]
    new_priority = new_priority if new_priority else task[3]
    new_due_date = new_due_date if new_due_date else task[4]

    # Update the task
    try:
        cursor.execute("UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ? AND user_id = ?", (new_title, new_description, new_status, new_priority, new_due_date, task_id, user_id))
        conn.commit()
        print("Task updated successfully.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Deleting task")
def delete_task(cursor, conn, user_id, current_user=None):
    # Display the user's tasks
    try:
        cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.priority, tasks.due_date, GROUP_CONCAT(users.username, ', ') as assignees
        FROM tasks
        JOIN task_assignments ON tasks.id = task_assignments.task_id
        JOIN users ON task_assignments.user_id = users.id
        WHERE task_assignments.user_id = ?
        GROUP BY tasks.id
        """, (user_id,))
        tasks = cursor.fetchall()
        if tasks:
            print("Your tasks:")
            for task in tasks:
                print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}, Priority: {task[4]}, Due Date: {task[5]}, Assigned to: {task[6]}")
        else:
            print("No tasks found.")
            return
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return

    # Ask for the task ID to delete
    task_id = input("Enter task ID to delete: ").strip()

    # Delete the task
    try:
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()
        print("Task deleted successfully.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Assigning task")
def assign_task(cursor, conn, current_user_id, current_user=None):
    # Display the current tasks
    try:
        cursor.execute("SELECT id, title FROM tasks WHERE user_id = ?", (current_user_id,))
        tasks = cursor.fetchall()
        if tasks:
            print("Current tasks:")
            for task in tasks:
                print(f"ID: {task[0]}, Title: {task[1]}")
        else:
            print("No tasks found.")
            return
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return

    # Ask for the task ID to assign
    task_id = input("Enter task ID to assign: ").strip()

    # Display the available users
    try:
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        if users:
            print("Available users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}")
        else:
            print("No users found.")
            return
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")
        return

    # Ask for the user IDs to assign the task to
    user_ids = input("Enter user IDs to assign the task to (comma-separated): ").strip().split(',')
    user_ids = [int(uid.strip()) for uid in user_ids]

    # Ask if the task should remain assigned to the current user
    keep_assigned = input("Keep the task assigned to you as well? (yes/no): ").strip().lower()
    if keep_assigned == 'yes':
        user_ids.append(current_user_id)

    # Assign the task to the specified users
    try:
        for user_id in user_ids:
            # Check if the task is already assigned to the user
            cursor.execute("SELECT * FROM task_assignments WHERE task_id = ? AND user_id = ?", (task_id, user_id))
            assignment = cursor.fetchone()
            if assignment:
                print(f"Task {task_id} is already assigned to user {user_id}.")
            else:
                cursor.execute("INSERT INTO task_assignments (task_id, user_id) VALUES (?, ?)", (task_id, user_id))
        conn.commit()
        print("Task assigned successfully.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")

@log_action("Deleting user")
def delete_user(cursor, conn, current_user=None):
    username = input("Enter the username of the user to delete: ").strip()
    
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"User '{username}' deleted successfully.")
    except sqlite3.Error as err:
        print(f"An error occurred: {err}")