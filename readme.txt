Task Management System with Access Control
Overview

Build a Task Management System where:

    Users can create, read, update, and delete (CRUD) tasks.
    The system uses decorators for access control and logging.
    Tasks are stored in a MySQL database.
    

Features

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
        All user and task data is stored in a MySQL database.
        Tasks are associated with users, ensuring personal data is kept private.

    Optional Enhancements:
        Add caching for frequently accessed tasks using functools.lru_cache.
        Implement additional features like task prioritization or due date reminders.

Key steps:

	Decorators:

    Implement an @auth_required decorator to enforce user authentication.
    Create a @log_action decorator to log every user interaction.

	Database Connection:

    Use MySQL to store and retrieve tasks.
    Create schemas, write SQL queries, and manage connections.

Libraries:

    mysql-connector-python (or SQLAlchemy for ORM)
    datetime (for task scheduling)
    functools (for decorators)