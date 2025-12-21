from fastapi import FastAPI, status, HTTPException, Depends
from typing import List

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.model import Base
from app.model import Post as post_table_model
from app.model import User as user_table_model

from app.routers import post, user, auth, vote
Base.metadata.create_all(engine)

from app.util import hash_password
from app.schema import PostCreate, UserPydanticCheck, UserResponseModel


from app.config import settings

# print(settings.SECRET_KEY)
# print(settings.path)

print(settings.secret_key)
print(settings.database_hostname)

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

origins=["*"]
# origins=["https://www.google.com", "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) # post is imported and router is defined inside post.py file
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



