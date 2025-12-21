from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLALCHEMY_BASELINE_URL = "postgresql://postgres:sitendra@localhost/fastapi"
SQLALCHEMY_BASELINE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# create the engine
engine = create_engine(SQLALCHEMY_BASELINE_URL)

# Session connection with engine
sessionLocal = sessionmaker( autoflush=False, autocommit=False, bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()


