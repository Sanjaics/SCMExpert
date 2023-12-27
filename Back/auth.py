# auth.py
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from Back.db import users
from fastapi import Request, Depends, Form, HTTPException, status, Cookie, Response
from fastapi import HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError
import asyncio
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()


# Load environment variables for JWT configuration
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

#token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

PASSWORD_HASH = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Getting hashpassword,verifypassword
class Hashpass:
    def create_user(password: str) -> str:
        return PASSWORD_HASH.hash(password)


    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PASSWORD_HASH.verify(plain_password, hashed_password)

#Generating token 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()     
    # token expiration time
    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    #encode the token 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#decode token Fun()
def decode_token(token: str):
    try:
        #decode the provided token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})



#Get user to access jwt
def get_current_user(token: str = Depends(oauth2_scheme)):
    # print(f"Received token: {token}")
    try:
        payload = decode_token(token)
        # print(payload)
        if payload and "email" in payload:
            # print("condition satisfied")
            user_data = users.find_one({"email": payload["email"]})
            # print(user_data)
            if user_data and "username" in user_data:
                return {"username": user_data["username"], "email": payload["email"],"role":user_data["role"]}
            # print(user_data)
    except JWTError as e:
      if "ExpiredSignatureError" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


#authenticating user 
async def authenticate_user(email: str, password: str):
    loop = asyncio.get_event_loop()
    user = await loop.run_in_executor(None, lambda: users.find_one({"email": email}))
    if not user or not Hashpass.verify_password(password, user['password']):
        return False
    return user

