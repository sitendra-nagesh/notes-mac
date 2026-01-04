from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    # created_at: datetime


class PostCreate(PostBase):
    # owner_id: int
    pass

class UserPydanticCheck(BaseModel):
    email: EmailStr
    password: str

class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    # class Config:
    #     from_attributes = True

class PostResponse(PostBase):
    owner: UserResponseModel

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   