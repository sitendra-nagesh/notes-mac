from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()

class PostTable(Base):
    __tablename__ = "pydantictable"
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, nullable=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class UserTable(Base):
    __tablename__ = "userstable"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")) 