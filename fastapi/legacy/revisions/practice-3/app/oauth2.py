from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schema
from fastapi import FastAPI, status, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from sqlalchemy.orm import Session
from app import database, model

from app.config import settings

# SECRET_KEY = 
# ALGROTHM = 
# EXPIRATION_TIME = 

#  openssl rand -hex 32

# SECRET_KEY = "2b67bea9a09d4e1a209d9348fba29724a6099fad53a8a86e048257fb4806e786"
# ALGORITHM = "HS256"
# EXPIRATION_TIME = 60
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str , credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id == None:
            raise credential_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user