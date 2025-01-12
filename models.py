# filepath: /c:/Users/mykal/Desktop/task_management_CLI/models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False)
    priority = Column(String, CheckConstraint("priority IN ('High', 'Medium', 'Low')"))
    due_date = Column(String)
    category = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="tasks")

User.tasks = relationship("Task", order_by=Task.id, back_populates="user")

def initialize_db():
    engine = create_engine('sqlite:///task_manager.db')
    Base.metadata.create_all(engine)
    print("Database initialization complete.")