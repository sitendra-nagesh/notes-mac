from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine, get_db
from app.model import Base
from app.model import Post as post_table_model
from app.model import User as user_table_model
from app.model import Vote as vote_table_model
from app import oauth2


from app.util import hash_password

from app.schema import PostCreate, UserPydanticCheck, UserResponseModel

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # all_posts = db.query(post_table_model).filter(post_table_model.owner_id == current_user.id).all()
    # print(limit)
    # print(search) # we use %20 to indicate the space in the search bar
    # all_posts = db.query(post_table_model).all()
    # all_posts = db.query(post_table_model).limit(limit=limit).offset(skip).all()
    all_posts = db.query(post_table_model).filter(post_table_model.title.contains(search)).limit(limit=limit).offset(skip).all()
    results = db.query(post_table_model, func.count(post_table_model.id).label("votes")).join(vote_table_model,  vote_table_model.post_id == post_table_model.id, isouter=True).group_by(post_table_model.id).all()
    # print(results)
    return results

@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    # new_post = post_table_model(title = post.title, content = post.content, owner_id = post.owner_id)
    new_post = post_table_model(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_a_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    print("one_post", one_post)
    if one_post == None:
        # raise HTTPException(status_code=404, detail=f"id {id} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist.")
        
    # if one_post.owner_id != current_user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    return one_post

@router.put("/{id}")
def update_a_post(id: int, post: PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    
    if one_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    db.query(post_table_model).filter(post_table_model.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(one_post)

    return one_post

@router.delete("/{id}", status_code = 201)
def delete_a_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    one_post = db.query(post_table_model).filter(post_table_model.id == id ).first()
    if one_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"id {id} does not exist.")
    
    if one_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    db.delete(one_post)
    db.commit()