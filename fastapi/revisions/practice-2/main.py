from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange

from database import get_db, Session, engine
import model
import schema
from model import Base

Base.metadata.create_all(engine)

class Posts(BaseModel):
    title: str
    content: str

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(model.PostTable).all()

@app.post("/posts")
def create_posts(post: schema.PostPydantic, db: Session = Depends(get_db)):
    # new_post = model.PostTable(title = post.title, content = post.content, published=post.published)
    new_post = model.PostTable(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_a_post(id: int, db: Session = Depends(get_db)):
    user = db.query(model.PostTable).filter(model.PostTable.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    return user

@app.put("/posts/{id}")
def update_a_post(id: int, post: schema.PostPydantic , db: Session = Depends(get_db)):
    update_post = db.query(model.PostTable).filter(model.PostTable.id == id).first()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    
    db.query(model.PostTable).filter(model.PostTable.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(update_post)
    return update_post
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(model.PostTable).filter(model.PostTable.id == id).first()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
    
    db.delete(delete_post)
    db.commit()
    

# USER Related endpoints

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserPydanticResponse)
def create_user(user: schema.UserPydantic, db: Session = Depends(get_db)):
    print(user)

    new_user = model.UserTable(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @app.get("/posts")
# def get_posts():
#     return post_list

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Posts):
#     post_dict = post.dict()
#     id = randrange(0, 10000000,1)
#     post_dict["id"] = id
#     post_list.append(post_dict)
#     return {"message": "post created successfully!"}

# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# def get_a_post(id: int):
#     idx = get_idx(id)
#     if idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" id {id} does not exist.")
#     return post_list[idx]

# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_a_post(id: int, post: Posts):
#     idx = get_idx(id)
#     if idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" id {id} does not exist.")
#     post_dict = post.dict()
#     post_dict["id"] = idx
#     post_list[idx] = post_dict
#     return {"message": "post update successfully!"}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def get_a_post(id: int):
#     idx = get_idx(id)
#     if idx == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" id {id} does not exist.")
#     del post_list[idx]