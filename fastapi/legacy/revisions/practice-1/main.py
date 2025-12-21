from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange

class PostsModel(BaseModel):
    title: str
    content: str

app = FastAPI()

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection to database using creating engine
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sitendra@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define the table which will be connected with engine
Base = declarative_base()
class User(Base):
    __tablename__ = "practicetwo"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

Base.metadata.create_all(engine)

# Set up session to connect with the table
Session = sessionmaker(bind=engine)
Session = Session()

# test the entry
# new_post = User(title = "Alice's post", content = "Content of Alices's post")

# Session.add(new_post)
# Session.commit()


@app.get("/posts")
def get_posts():
    post_list = Session.query(User).all()
    return post_list

@app.post("/posts")
def create_post(post: PostsModel):
    new_post = User(title = post.title, content = post.content)
    Session.add(new_post)
    Session.commit()
    return post

@app.put("/posts/{id}")
def update_post(id: int, post: PostsModel):
    updated_post = Session.query(User).filter(User.id == id).first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    updated_post.title = post.title
    update_post.content = post.content
    Session.commit()
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = Session.query(User).filter(User.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    Session.delete(deleted_post)
    Session.commit()

Session.close()

# import psycopg2
# from psycopg2.extras import RealDictCursor

# try:
#     conn = psycopg2.connect(host="localhost", port=5432, password="sitendra", database="fastapi", user="postgres", cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("connected to postgress successfully")
# except Exception as e:
#     print(e)
#     print("unable to connect to postgresql")


# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM pracone;")
#     all_posts = cursor.fetchall()
#     return all_posts
    

# @app.post("/posts")
# def create_posts(post: PostsModel):
#     cursor.execute("INSERT INTO pracone (title, content) VALUES (%s, %s)", (post.title, post.content))
#     conn.commit()
#     return {"message": "new is created successfully!"}

# @app.get("/posts/{id}")
# def get_one_post(id: int):
#     cursor.execute("SELECT * FROM pracone WHERE id = %s;", (str(id)))
#     post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
#     return post

# @app.put("/posts/{id}")
# def update_post(id: int, post: PostsModel):
#     cursor.execute("SELECT * FROM pracone WHERE id = %s", (str(id)))
#     response = cursor.fetchone()

#     if response == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")

#     cursor.execute("UPDATE pracone SET title = %s, content = %s WHERE id = %s;", (post.title, post.content, str(id)))
#     conn.commit()
    
#     return {"message": "updated successfully"}

# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     cursor.execute("SELECT * FROM pracone WHERE id = %s", (str(id)))
#     response = cursor.fetchone()
#     if response == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    
#     cursor.execute("DELETE FROM pracone WHERE id = %s", (str(id)))
#     conn.commit()

#     return {"message": "delete successfully"}


# "INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def")

# post_list = [
#     {"title": "first post", "content": "content of first post", "id": 1},
#     {"title": "second post", "content": "content of second post", "id": 2},
# ]

# def get_idx(id):
#     for idx, elm in enumerate(post_list):
#         if id == elm["id"]:
#             return idx
#     return None

# @app.get("/posts", status_code=status.HTTP_200_OK)
# def get_posts():
#     cursor.execute("SELECT * FROM pracone")
#     post_list = cursor.fetchall()
#     return post_list

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: PostsModel):
#     print(post)
#     postDictFormat = post.dict()
#     id = randrange(0,10000000,1)
    
#     postDictFormat["id"] = id
#     post_list.append(postDictFormat)

#     return postDictFormat

# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# def get_post_by_id(id: int):
#     idx = get_idx(id)
#     if  idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} element does not exist")
#     return post_list[idx]

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     idx = get_idx(id)
#     if idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
#     del post_list[idx]

# @app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
# def update_post(id: int, post: PostsModel):
#     idx = get_idx(id)
#     if idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
#     postDictFormat = post.dict()
#     postDictFormat["id"] = id
#     post_list[idx] = postDictFormat
#     return postDictFormat