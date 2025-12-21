from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()
my_posts = [
    {"title": "my post 1", "content": "content of my post 1", "id": 1},
    {"title": "my post 2", "content": "content of my post 2", "id": 2}
    ]

class Response(BaseModel):
        id: int
        # title: str
        content: str

def get_idx(id):
    for idx,post in enumerate(my_posts):
        if post["id"] == id:
            return idx

@app.get("/posts", status_code=status.HTTP_201_CREATED, response_model=List[Response])
def list_all_posts():
    return my_posts

@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Response)
def get_post(id: int):
    idx = get_idx(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="${id} does not exist")
    return my_posts[idx]

