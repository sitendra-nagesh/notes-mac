from fastapi import FastAPI
from pydantic import BaseModel 

class Posts(BaseModel):
    title: str
    id: int

app = FastAPI()

post_list = [
        {"title": "first title", "id": 1},
        {"title": "second title", "id": 2},
        ]

@app.get("/posts")
def get_post():
    #print(post_list)
    #return {"message": "Hello"} 
    return post_list

@app.post("/posts")
def create_post(post: Posts):
    post = post.dict()
    print(post)
    post_list.append(post)
    return {"post is successfully created"} 




