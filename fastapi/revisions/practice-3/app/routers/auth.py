from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schema import LoginModel
from app.model import User
from app.database import get_db
from app.oauth2 import create_access_token
from app import util

router = APIRouter(
    tags = ["authentication"]
)

@router.post("/login")
# def check_user(user_auth: LoginModel, db: Session = Depends(get_db)):
def check_user(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # check if email exists
    credentials_from_table = db.query(User).filter(User.email == user_auth.username).first()
    # print(credentials_from_table.email, credentials_from_table.password)
    if credentials_from_table == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credentials")
    
    # validate the password
    if not util.verify(user_auth.password, credentials_from_table.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credentials")

    # create the token and share
    created_token = create_access_token(data={"user_id": credentials_from_table.id})
    return {"access token": created_token, "token_type": "bearer token"}
