from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Engine: The starting point; it connects to your database.
# Base: A declarative base class for defining your models.
# Model: A Python class that represents a database table.
# Session: Manages conversations with the database (like adding, querying, committing changes).
# Query: How you retrieve data.
# CRUD: Create, Read, Update, Delete operations.

# Engine: The starting point, it connects to your database
# Base: A declarative base for defining your models
# Model: A python class that represents a database table
# Session: Manages conversations with the databse (like adding, querying, commiting changes).
# Query: How you retrieve data.

# Engine: This helps in connecting with database
# Base: It is base class from sqlalchemy to be used to define tables/models
# Model: a class for defining table
# Session: a session is for cummincating with database

engine = create_engine('sqlite:///mydatabase.db', echo=True)  # echo=True logs SQL for learning

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Primary key, auto-increments
    name = Column(String)  # String column
    age = Column(Integer)  # Integer column

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

new_user = User(name="Alice", age=30)

session.add(new_user)

session.commit()

session.close()

session = Session()

users = session.query(User).all()

for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

session.close()
