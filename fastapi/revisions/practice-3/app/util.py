from passlib.context import CryptContext
myctx = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return myctx.hash(password)