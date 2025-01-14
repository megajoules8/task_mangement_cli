This is an ongoing project I am currently working on for a student to give them examples of a few concepts and hopefully inspire their own project extension.
It has been updated from using direct SQLlite database queries to using SQLAlchemy as the ORM. 
It's all still a work in progress. 

Task Management System with Access Control
Overview

Build a Task Management System where:

    Users can create, read, update, and delete (CRUD) tasks.
    The system uses decorators for access control and logging.
    Tasks are stored in a SQLlite database.
    

Features:

    User Authentication:
        Users can log in to access their personal tasks.
        Authentication is enforced using a decorator (@auth_required).
        If a user is not logged in, they cannot access the system.

    Task CRUD Operations:
        Create Task: Add a new task (e.g., "Prepare report for Monday").
        Read Task: View a list of tasks, optionally filtering by status (e.g., "pending" tasks).
        Update Task: Update a task’s status (e.g., from "pending" to "completed").
        Delete Task: Remove a task from the system.

    Action Logging:
        Every action (e.g., creating, reading, or deleting a task) is logged using a decorator (@log_action).

    Database Integration:
        All user and task data is stored in a SQLite database using SQLAlchemy as the ORM.
        Tasks are associated with users, ensuring personal data is kept private.

    Optional Enhancements:
        Add caching for frequently accessed tasks using functools.lru_cache.
        Implement additional features like task prioritization or due date reminders.

