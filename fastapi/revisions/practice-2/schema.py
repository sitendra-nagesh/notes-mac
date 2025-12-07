from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostPydantic(BaseModel):
    title: str
    content: str
    published: bool = False
    # created_at: datetime

class UserPydantic(BaseModel):
    email: EmailStr
    password: str

class UserPydanticResponse(BaseModel):
    email: EmailStr
    created_at: datetime