from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Task
from db_connection import connect_to_db
from decorators import auth_required, log_action

session = connect_to_db()

@log_action("Logging in")
def login(username, password):
    try:
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            print("Login successful.")
            return user
        else:
            print("Invalid username or password.")
            return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

@log_action("Registering user")
def register(username, password):
    try:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        print("User registered successfully.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()

@log_action("Logging out")
def logout():
    print("Logged out successfully.")

@auth_required
@log_action("Creating task")
def create_task(user_id, current_user=None):
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    status = input("Enter task status: ").strip()
    
    while True:
        priority = input("Enter task priority (High, Medium, Low): ").strip().capitalize()
        if priority in ['High', 'Medium', 'Low']:
            break
        print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")
    
    due_date = input("Enter task due date (YYYY-MM-DD): ").strip()
    category = input("Enter task category: ").strip()
    
    try:
        task = Task(title=title, description=description, status=status, priority=priority, due_date=due_date, category=category, user_id=user_id)
        session.add(task)
        session.commit()
        print("Task created successfully.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()

@auth_required
@log_action("Viewing tasks")
def view_tasks(user_id, current_user=None):
    try:
        tasks = session.query(Task).filter_by(user_id=user_id).all()
        for task in tasks:
            print(f"ID: {task.id}, Title: {task.title}, Status: {task.status}, Priority: {task.priority}, Due Date: {task.due_date}, Category: {task.category}")
    except Exception as err:
        print(f"An error occurred: {err}")

@log_action("Viewing all tasks")
def view_all_tasks():
    try:
        tasks = session.query(Task).all()
        for task in tasks:
            print(f"ID: {task.id}, Title: {task.title}, Status: {task.status}, Priority: {task.priority}, Due Date: {task.due_date}, Category: {task.category}")
    except Exception as err:
        print(f"An error occurred: {err}")

@auth_required
@log_action("Updating task")
def update_task(task_id, current_user=None):
    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            task.title = input(f"Enter new title (current: {task.title}): ").strip() or task.title
            task.description = input(f"Enter new description (current: {task.description}): ").strip() or task.description
            task.status = input(f"Enter new status (current: {task.status}): ").strip() or task.status
            task.priority = input(f"Enter new priority (current: {task.priority}): ").strip() or task.priority
            task.due_date = input(f"Enter new due date (current: {task.due_date}): ").strip() or task.due_date
            task.category = input(f"Enter new category (current: {task.category}): ").strip() or task.category
            session.commit()
            print("Task updated successfully.")
        else:
            print("Task not found.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()

@auth_required
@log_action("Deleting task")
def delete_task(task_id, current_user=None):
    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
            print("Task deleted successfully.")
        else:
            print("Task not found.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()

@auth_required
@log_action("Assigning task")
def assign_task(task_id, user_id, current_user=None):
    try:
        task = session.query(Task).filter_by(id=task_id).first()
        user = session.query(User).filter_by(id=user_id).first()
        if task and user:
            task.user_id = user_id
            session.commit()
            print("Task assigned successfully.")
        else:
            print("Task or user not found.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()

@auth_required
@log_action("Deleting user")
def delete_user(user_id, current_user=None):
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"User '{user.username}' deleted successfully.")
        else:
            print("User not found.")
    except Exception as err:
        print(f"An error occurred: {err}")
        session.rollback()