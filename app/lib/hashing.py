from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"])

def hash_password(plain_pwd)->str:
    return pwd_context.hash(plain_pwd)

def verify_password(plain_pwd:str,hashed_pwd:str)->bool:
    return pwd_context.verify(plain_pwd,hashed_pwd)