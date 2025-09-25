from fastapi import FastAPI, HTTPException, status

app = FastAPI()

post_list = [
        {"title": "title 1 of the post", "id": 1},
        {"title": "title 2 of the post", "id": 2},
        ]
def get_post_by_id(id):
    for idx, post in enumerate(post_list):
        if post["id"] == id: 
            return idx


@app.get("/posts")
def get_posts():
    return post_list

@app.get("/posts/{id}")
def get_post(id: int):
    idx = get_post_by_id(id) 
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} does not exist")

    return post_list[idx]
