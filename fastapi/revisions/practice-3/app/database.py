from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_BASELINE_URL = "postgresql://postgres:sitendra@localhost/fastapi"
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


