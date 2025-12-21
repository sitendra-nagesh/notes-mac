from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sitendra@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# connect sesssion with table. 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()