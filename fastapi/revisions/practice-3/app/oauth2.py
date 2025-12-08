from jose import JWTError, jwt
from datetime import datetime, timedelta
# SECRET_KEY = 
# ALGROTHM = 

# EXPIRATION_TIME = 

#  openssl rand -hex 32

SECRET_KEY = "2b67bea9a09d4e1a209d9348fba29724a6099fad53a8a86e048257fb4806e786"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt