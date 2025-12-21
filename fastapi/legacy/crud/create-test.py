from fastapi import FastAPI, HTTPException, status
from random import randrange
from pydantic import BaseModel


post_list = [
            { "title": "my post 1", "id": 1, "content": "content of post 1"},
            { "title": "my post 2", "id": 2, "content": "content of post 2"},
        ]

app = FastAPI()

class Posts(BaseModel):
    title: str
    id: int
    content: str = None

def get_post_by_id(id):
    for idx, post in enumerate(post_list):
        if id == post["id"]:
            return idx


@app.get("/posts")
def get_posts():
    return post_list

@app.get("/posts/{id}")
def get_post(id: int):
    
    idx = get_post_by_id(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist.")
    return post_list[idx]

@app.post("/posts")
def create_posts(post_response: Posts):
    id = randrange(1000000)
    post_response = post_response.dict()
    post_response["id"] = id
    post_list.append(post_response) 
    return {"message": f"your post is created with id: {id}"}

@app.put("/posts/{id}")
def update_post(post_response: Posts, id: int):
    idx = get_post_by_id(id)
    if idx == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    post_list[idx] = post_response.dict()
    post_list[idx]["id"] = id
    return {"message": f"your post with id {id} is updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    idx = get_post_by_id(id)
    if idx == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    del post_list[idx]
    return {"message": "post is successfully deleted"}

