from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from random import randrange

# postgres connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# postgresql using sqlalchemy
from database import engine, get_db
import models
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(database="fastapi", user="postgres", port = 5432)
        curr = conn.cursor(cursor_factory=RealDictCursor)
        print("Successfully connected with postgres")
        break
    except Exception as e:
        time.sleep(2)
        print("Unable to connect with postgress")
        print(e)


class Posts(BaseModel):
    title: str
    content: str
    id: int = None

app = FastAPI()

post_list = [
    {"title": "first post", "content": "content of first post", "id": 1 },
    {"title": "second post", "content": "content of second post", "id": 2 },
]

def get_post_idx(id):
    for idx, item in enumerate(post_list):
        if item["id"] == id:
            return idx

# @app.get("/postgres")
# def get_postgres_posts():
#     curr.execute("SELECT * FROM practice01")
#     post_list = curr.fetchall()
#     return post_list

# @app.get("/sqlalchemy")
# def hello_sqlalchemy(db: Session = Depends(get_db)):
#     query = db.query(models.Posts)
#     print(query)
#     return query.all()
    

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    post_list = db.query(models.Posts).all()
    # curr.execute("SELECT * FROM practice01")
    # post_list = curr.fetchall() 
    return post_list

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # curr.execute("SELECT * FROM practice01 WHERE id = %s", (str(id),))
    # post = curr.fetchone()
    one_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not one_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} does not exist")
    # idx = get_post_idx(id)
    # if idx == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} does not exist")
    return one_post

@app.post("/posts")
def create_post(post: Posts, db: Session = Depends(get_db)):
    # id = randrange(0, 10000000)
    # new_post = post.dict()
    # new_post["id"] = id
    # post_list.append(new_post)
    # return new_post

    # curr.execute("INSERT INTO practice01 (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content,))
    # new_post = curr.fetchone()
    # conn.commit()
    # new_post = models.Posts(title = post.title, content = post.content)
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}")
def update_post(id: int, post: Posts, db: Session = Depends(get_db)):
    # curr.execute("SELECT * FROM practice01 WHERE id = %s", (str(id),))
    # updated_post = curr.fetchone()
    # idx = get_post_idx(id)
    selected_post = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = selected_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} does not exist")
    # post_list[idx] = post.dict()
    # post_list[idx]["id"] = id
    # return post_list[idx]
    # curr.execute("UPDATE practice01 SET title = %s ,  content = %s WHERE id = %s RETURNING *; ", (post.title, post.content, str(id)))
    # new_post = curr.fetchone()
    # conn.commit()
    post_dict = post.dict()
    post_dict["id"] = id
    selected_post.update(post_dict)

    db.commit()
    new_post = selected_post.first()
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # idx = get_post_idx(id)
    # print(idx)
    # curr.execute("DELETE FROM practice01 WHERE id = %s RETURNING * ;" , (str(id)))
    # deleted_post = curr.fetchone()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist")
    db.delete(deleted_post)
    db.commit()

