from fastapi import FastAPI, HTTPException, status, Response
from random import randrange
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time

post_list = [
            { "title": "my post 1", "id": 1, "content": "content of post 1"},
            { "title": "my post 2", "id": 2, "content": "content of post 2"},
        ]

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

def get_post_by_id(id):
    for idx, post in enumerate(post_list):
        if id == post["id"]:
            return idx

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts;")
    post_list = cursor.fetchall()
    return post_list

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    response = cursor.fetchone()
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    return response

@app.post("/posts")
def create_posts(post_response: Posts):
    cursor.execute("""INSERT INTO posts (title, content, published ) VALUES (%s, %s, %s) RETURNING *""", (post_response.title, post_response.content, post_response.published))
    post_return = cursor.fetchone()
    conn.commit()
    return post_return

@app.put("/posts/{id}")
def update_post(post_response: Posts, id: int):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post_response.title, post_response.content, post_response.published, str(id),))
    resp = cursor.fetchone()
    if not resp:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    conn.commit()
    return {"data": resp}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    response = cursor.fetchone()
    conn.commit()
    if response == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)