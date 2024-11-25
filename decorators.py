# decorators.py
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if not current_user:
            print("You must be logged in to perform this action.")
            return
        return func(*args, **kwargs)
    return wrapper

def log_action(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Action: {action}")
            return func(*args, **kwargs)
        return wrapper
    return decorator