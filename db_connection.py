# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///task_manager.db')
Session = sessionmaker(bind=engine)

def connect_to_db():
    try:
        print("Connecting to the database...")
        session = Session()
        print("Connection successful")
        return session
    except Exception as err:
        print(f"Error: {err}")
        return None
