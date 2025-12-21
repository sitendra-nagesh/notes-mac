# from passlib.context import CryptContext
# myctx = CryptContext(schemes=["bcrypt"])

# def hash_password(password):
#     return myctx.hash(password)

# def verify(plain_password, hash_password):
#     return myctx.verify(plain_password, hash_password)

# Source - https://stackoverflow.com/a
# Posted by Marcello Herreshoff
# Retrieved 2025-12-07, License - CC BY-SA 4.0

import bcrypt
bcrypt.__about__ = bcrypt

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password1):
    return pwd_context.verify(plain_password, hashed_password1)