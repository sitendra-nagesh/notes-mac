from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

# Steps to run this app
# fastapi dev main.py
