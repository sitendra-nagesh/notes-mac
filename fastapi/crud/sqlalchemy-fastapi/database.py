# this will define the connection with database and session to connect with database and just a base class variable
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection to database using creating engine
SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Getting session pool to connect with connection
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defining table using base model
Base = declarative_base()

# querying the table or crud operation
# a file called models.py will contain the changes

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()