from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.model import Base
from app.model import Post as post_table_model
from app.model import User as user_table_model

from app.util import hash_password

from app.schema import PostCreate, UserPydanticCheck, UserResponseModel

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

# user table
@router.get("/", response_model = List[UserResponseModel] )
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(user_table_model).all()
    return all_users

@router.get("/{id}", response_model = UserResponseModel )
def get_a_user(id: int, db: Session = Depends(get_db), response_model = UserResponseModel):
    
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    return new_user

@router.post("/", response_model = UserResponseModel)
def create_user(user: UserPydanticCheck, db: Session = Depends(get_db)):
    # print(user, user.password)
    user.password = hash_password(user.password)
    new_user = user_table_model(email = user.email, password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", status_code=204)
def get_a_user(id: int, db: Session = Depends(get_db)):
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    db.delete(new_user)
    db.commit()

@router.put("/{id}", status_code=201, response_model = UserResponseModel)
def get_a_user(user: UserPydanticCheck, id: int, db: Session = Depends(get_db)):
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    db.query(user_table_model).filter(user_table_model.id == id).update(user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(new_user)
    return new_user