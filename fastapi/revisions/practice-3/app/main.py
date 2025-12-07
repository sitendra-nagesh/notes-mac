from fastapi import FastAPI, status, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.model import Base
from app.model import Post as post_table_model
from app.model import User as user_table_model

from app.routers import post, user
Base.metadata.create_all(engine)

from app.util import hash_password

from app.schema import PostCreate, UserPydanticCheck, UserResponseModel

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)



