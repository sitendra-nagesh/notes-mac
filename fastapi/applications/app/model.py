from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy.orm import relationship
Base = declarative_base()

class Post(Base):
    __tablename__ = "poststwo"
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("userstwo.id", ondelete="CASCADE"), nullable=False)
    # owner=relationship("User") # User class 

class User(Base):
    __tablename__ = "userstwo"
    id = Column(Integer, primary_key=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    # phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votestwo"
    user_id = Column(Integer, ForeignKey("userstwo.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("poststwo.id", ondelete="CASCADE"), primary_key=True)