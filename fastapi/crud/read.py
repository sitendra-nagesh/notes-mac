from fastapi import FastAPI

app = FastAPI()

all_posts = [
        {"title": "first title", "id": 1},
        {"title": "second title", "id": 2}
        ]

@app.get("/posts")
def read_all_posts():
    return all_posts
