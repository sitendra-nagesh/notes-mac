from fastapi import FastAPI, HTTPException, status

app = FastAPI()

all_posts = [
        {"title": "first title", "id": 1},
        {"title": "second title", "id": 2}
        ]

def get_post_by_id(id):
    for idx, post in enumerate(all_posts):
        if post["id"] == id:
            return idx
    return None

@app.get("/posts")
def read_all_posts():
    return all_posts

# Read only one post
@app.get("/posts/{id}")
def read_one_post(id: int):
    idx = get_post_by_id(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id :{id} does not exist")
    return get_post_by_id(id)
