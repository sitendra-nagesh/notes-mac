from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Engine
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Base
Base = declarative_base()

# Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Create tables
Base.metadata.create_all(engine)

# Session factory
Session = sessionmaker(bind=engine)

# Example operations
session = Session()

# Add
new_user = User(name='Bob', age=25)
session.add(new_user)
session.commit()

# Query
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

session.close()
