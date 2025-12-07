from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()

class Post(Base):
    __tablename__ = "testtablenameone"
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class User(Base):
    __tablename__ = "usertablenameone"
    id = Column(Integer, primary_key=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
