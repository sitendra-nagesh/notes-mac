from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes=True

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        # orm_mode = True
        from_attributes = True


# class Post(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool = False
#     created_at: datetime

#     class Config:
#         orm_mode=True
# class PostUpdate(PostBase):
#     pass


# class Posts(BaseModel):
#     title: str
#     content: str
#     published: bool = False

# class CreatePosts(BaseModel):
#     title: str
#     content: str
#     published: bool = False

# class UpdatePosts(BaseModel):
#     title: str
#     content: str
#     published: bool = False

