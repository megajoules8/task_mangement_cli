#print("Script is running!")  # Add this at the top of main.py
from db_connection import connect_to_db
from operations import login, register, logout, create_task, view_tasks, view_all_tasks, update_task, delete_task, assign_task, delete_user

# Global variable to track the logged-in user
current_user = None

def show_menu():
    """Display the main menu options."""
    print("""
    Welcome to Task Manager!
    1. Log in
    2. Register new user
    3. View My Tasks
    4. View All Tasks
    5. Create Task
    6. Update Task
    7. Delete Task
    8. Assign Task
    9. Logout
    10. Exit
    11. Delete User
    """)

def main():
    """Main program loop."""
    global current_user

    try:
        print("Attempting to connect to the database...")
        # Establish database connection
        conn, cursor = connect_to_db()
        if not conn or not cursor:
            print("Failed to connect to the database. Exiting...")
            return
        print("Connected to the database.")

        while True:
            show_menu()
            choice = input("Choose an option: ").strip()
            print(f"User selected option: {choice}")

            if choice == "1":  # Log in
                current_user = login(cursor)
                print(f"Current user: {current_user}")
            elif choice == "2":  # Register
                register(cursor, conn)
            elif choice == "3":  # View My Tasks
                if current_user:
                    view_tasks(cursor, user=current_user, current_user=current_user)
                else:
                    print("You must be logged in to view tasks.")
            elif choice == "4":  # View All Tasks
                view_all_tasks(cursor, current_user=current_user)
            elif choice == "5":  # Create a task
                if current_user:
                    user_id = current_user[0]  # Extract user ID from the tuple
                    create_task(cursor, conn, user_id, current_user=current_user)
                else:
                    print("You must be logged in to create a task.")
            elif choice == "6":  # Update a task
                if current_user:
                    user_id = current_user[0]  # Extract user ID from the tuple
                    update_task(cursor, conn, user_id, current_user=current_user)
                else:
                    print("You must be logged in to update a task.")
            elif choice == "7":  # Delete a task
                if current_user:
                    user_id = current_user[0]  # Extract user ID from the tuple
                    delete_task(cursor, conn, user_id, current_user=current_user)
                else:
                    print("You must be logged in to delete a task.")
            elif choice == "8":  # Assign a task
                if current_user:
                    user_id = current_user[0]  # Extract user ID from the tuple
                    assign_task(cursor, conn, user_id, current_user=current_user)
                else:
                    print("You must be logged in to assign a task.")
            elif choice == "9":  # Logout
                if current_user:
                    logout()
                    current_user = None
                else:
                    print("You are not logged in.")
            elif choice == "10":  # Exit
                print("Exiting the Task Manager. Goodbye!")
                break
            elif choice == "11":  # Delete User
                if current_user:
                    delete_user(cursor, conn, current_user=current_user)
                else:
                    print("You must be logged in to delete a user.")
            else:
                print("Invalid choice. Please try again.")
        # Close the database connection
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Starting the Task Manager CLI...")
    main()
    print("Task Manager CLI has exited.")