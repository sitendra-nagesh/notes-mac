from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel

import models
from database import engine, get_db
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)
import utils

import schemas
from typing import Optional, List

app = FastAPI()

@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    query = db.query(models.Post).all()
    return query

@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(id == models.Post.id).first()
    if query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="${id} does not exist.")
    return query

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    selected_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = selected_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    selected_post.update(post_dict)
    db.commit()
    new_post = selected_post.first()
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist")
    db.delete(deleted_post)
    db.commit()

# @app.post("/users", status_code=status.HTTP_201_CREATED)
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_new(user: schemas.User ,db: Session = Depends(get_db)):
    print("user.password", user.password)
    hashed_pwd = utils.hash(user.password)
    print("hashed password", hashed_pwd)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    # print("from user:",user.email)
    # query = db.query(models.Post).filter(2 == models.Post.id).first()
    # print("from db:", query)
    db.commit()
    db.refresh(new_user)
    print("new_user:", new_user)
    return new_user
