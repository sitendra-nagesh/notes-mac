from fastapi import FastAPI, HTTPException, status, Response, Depends
from random import randrange
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time

# sqlalchemy
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="fastapi", user="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection faild")
        print("Error: ", error)
        time.sleep(2)

class Posts(BaseModel):
    title: str
    id: int = None
    published: bool = False
    content: str 

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    post_list = db.query(models.Posts).all()
    return post_list

# users = session.query(User).all() 
# for user in users:
#   print(f”ID: {user.id}, Name: {user.name}, Age: {user.age}”)

# new_user = User(name=’Alice’, age=30)
# session.add(new_user)
# session.commit()

# id = Column(Integer, primary_key=True, nullable=False)
# title = Column(String, nullable = False)
# content = Column(String, nullable = False)
# published = Column(Boolean, server_default = "TRUE", nullable = False)
# created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


# new_user = models.Posts(id = post_response.id, title = post_response.title , content = post_response.content , published = post_response.published)
# db.add(new_user)
# db.commit()


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts;")
    # post_list = cursor.fetchall()
    post_list = db.query(models.Posts).all()
    # print("db.query(models.Posts).all()", db.query(models.Posts)) to check the query used here. 
    return post_list

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # response = cursor.fetchone()
    # if not response:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    response = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    return response

@app.post("/posts")
def create_posts(post_response: Posts, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published ) VALUES (%s, %s, %s) RETURNING *""", (post_response.title, post_response.content, post_response.published))
    # post_return = cursor.fetchone()
    # conn.commit()
    # new_user = models.Posts(title = post_response.title , content = post_response.content , published = post_response.published)
    new_user = models.Posts(**post_response.dict())
    db.add(new_user)

    db.commit()
    db.refresh(new_user)
    return new_user

# @app.put("/posts/{id}")
# def update_post(post_response: Posts, id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post_response.title, post_response.content, post_response.published, str(id),))
#     # resp = cursor.fetchone()
#     # if not resp:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
#     # conn.commit()
#     updated_post = db.query(models.Posts).filter(models.Posts.id == id)
#     post = updated_post.first()
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
#     updated_post.update(post_response.dict(), synchronize_session = False)
#     db.commit()
#     return {"data": updated_post.first()}

@app.put("/posts/{id}")
def update_post(post_response: Posts, id: int, db: Session = Depends(get_db)):
    q = db.query(models.Posts).filter(models.Posts.id == id)
    existing = q.first()
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")

    update_data = post_response.dict(exclude_unset=True)  # only fields provided by client
    update_data.pop("id", None)                           # remove id if present

    q.update(update_data, synchronize_session=False)
    db.commit()

    return {"data": q.first()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # response = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
