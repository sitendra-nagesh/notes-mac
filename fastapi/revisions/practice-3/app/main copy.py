from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from database import engine, get_db

from model import Base
from model import Post as post_table_model
from model import User as user_table_model
Base.metadata.create_all(engine)

from util import hash_password

from schema import PostCreate, UserPydanticCheck, UserResponseModel

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(post_table_model).all()
    return all_posts

@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = post_table_model(title = post.title, content = post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_a_post(id: int, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    print("one_post", one_post)
    if one_post == None:
        # raise HTTPException(status_code=404, detail=f"id {id} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    return one_post

@app.put("/posts/{id}")
def update_a_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    
    db.query(post_table_model).filter(post_table_model.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(one_post)

    return one_post

@app.delete("/posts/{id}", status_code = 201)
def delete_a_post(id: int, db: Session = Depends(get_db)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    db.delete(one_post)
    db.commit()

# user table
@app.get("/users", response_model = List[UserResponseModel] )
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(user_table_model).all()
    return all_users

@app.get("/users/{id}", response_model = UserResponseModel )
def get_a_user(id: int, db: Session = Depends(get_db), response_model = UserResponseModel):
    
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    return new_user

@app.post("/users", response_model = UserResponseModel)
def create_user(user: UserPydanticCheck, db: Session = Depends(get_db)):
    # print(user, user.password)
    user.password = hash_password(user.password)
    new_user = user_table_model(email = user.email, password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.delete("/users/{id}", status_code=204)
def get_a_user(id: int, db: Session = Depends(get_db)):
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    db.delete(new_user)
    db.commit()

@app.put("/users/{id}", status_code=201, response_model = UserResponseModel)
def get_a_user(user: UserPydanticCheck, id: int, db: Session = Depends(get_db)):
    new_user = db.query(user_table_model).filter(user_table_model.id == id).first()
    if new_user == None:
        raise HTTPException(status_code = 404, detail = f"id {id} does not exist.")
    db.query(user_table_model).filter(user_table_model.id == id).update(user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(new_user)
    return new_user