from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy.orm import relationship
Base = declarative_base()

class Post(Base):
    __tablename__ = "testtablenameone"
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("usertablenameone.id", ondelete="CASCADE"), nullable=False)
    # owner=relationship("User") # User class 

class User(Base):
    __tablename__ = "usertablenameone"
    id = Column(Integer, primary_key=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votesone"
    user_id = Column(Integer, ForeignKey("usertablenameone.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("testtablenameone.id", ondelete="CASCADE"), primary_key=True)