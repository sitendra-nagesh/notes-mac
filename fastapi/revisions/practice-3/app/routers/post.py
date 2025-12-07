from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List


from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.model import Base
from app.model import Post as post_table_model
from app.model import User as user_table_model


from app.util import hash_password

from app.schema import PostCreate, UserPydanticCheck, UserResponseModel

router = APIRouter()

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(post_table_model).all()
    return all_posts

@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = post_table_model(title = post.title, content = post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}")
def get_a_post(id: int, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    print("one_post", one_post)
    if one_post == None:
        # raise HTTPException(status_code=404, detail=f"id {id} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    return one_post

@router.put("/posts/{id}")
def update_a_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    
    db.query(post_table_model).filter(post_table_model.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(one_post)

    return one_post

@router.delete("/posts/{id}", status_code = 201)
def delete_a_post(id: int, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    db.delete(one_post)
    db.commit()