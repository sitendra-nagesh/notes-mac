from fastapi import FastAPI
from pydantic import BaseModel



class Post(BaseModel):
    title : str
    content : str

post_list = []

app = FastAPI()

@app.get("/")
def root():
    return {"message": "I am at root"}

@app.post("/posts")
def create_post(post: Post):
    print(post)
    return {"message": "post created succcessfully"}
