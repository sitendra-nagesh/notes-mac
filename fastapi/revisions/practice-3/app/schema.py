from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    # created_at: datetime


class PostCreate(PostBase):
    pass

class UserPydanticCheck(BaseModel):
    email: EmailStr
    password: str

class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    # class Config:
    #     from_attributes = True

class LoginModel(BaseModel):
    email: EmailStr
    password: str
