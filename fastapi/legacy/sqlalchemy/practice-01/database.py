from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


URL = "postgresql://postgres@localhost/fastapi"
engine = create_engine(URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

