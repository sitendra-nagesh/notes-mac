

from sqlalchemy import Column, String, Integer, Boolean
from database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Posts(Base):
    __tablename__ = "practice02"
    id = Column(Integer, nullable = False,  primary_key = True)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = "FALSE")
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()") )
