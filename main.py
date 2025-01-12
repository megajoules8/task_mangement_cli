from db_connection import connect_to_db
from operations import login, register, logout, create_task, view_tasks, view_all_tasks, update_task, delete_task, assign_task, delete_user
from models import initialize_db

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
    global current_user
    initialize_db()
    print("Starting the Task Manager CLI...")
    session = connect_to_db()
    
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            current_user = login(username, password)
        elif choice == '2':
            username = input("Enter new username: ").strip()
            password = input("Enter new password: ").strip()
            register(username, password)
        elif choice == '3':
            if current_user:
                view_tasks(current_user.id, current_user=current_user)
            else:
                print("Please log in first.")
        elif choice == '4':
            view_all_tasks()
        elif choice == '5':
            if current_user:
                create_task(current_user.id, current_user=current_user)
            else:
                print("Please log in first.")
        elif choice == '6':
            if current_user:
                task_id = int(input("Enter task ID to update: ").strip())
                update_task(task_id, current_user=current_user)
            else:
                print("Please log in first.")
        elif choice == '7':
            if current_user:
                task_id = int(input("Enter task ID to delete: ").strip())
                delete_task(task_id, current_user=current_user)
            else:
                print("Please log in first.")
        elif choice == '8':
            if current_user:
                task_id = int(input("Enter task ID to assign: ").strip())
                user_id = int(input("Enter user ID to assign to: ").strip())
                assign_task(task_id, user_id, current_user=current_user)
            else:
                print("Please log in first.")
        elif choice == '9':
            logout()
            current_user = None
        elif choice == '10':
            print("Exiting Task Manager CLI.")
            break
        elif choice == '11':
            if current_user:
                user_id = int(input("Enter user ID to delete: ").strip())
                delete_user(user_id, current_user=current_user)
            else:
                print("Please log in first.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    initialize_db()
    main()