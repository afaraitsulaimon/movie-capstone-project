from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from jose import  JWTError, jwt
import database

import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from model import models


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY = os.environ.get('SECRET_KEY')
# ALGORITHM = os.environ.get('ALGORITH')
# ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')


SECRET_KEY = "djdh327r38j23h8723yejfnsdmsdj&&%%$@@%)hdbfhsdhfdfhd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire_time})

    # to create the jwt token
    jwt_encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded

def verify_access_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        idOfUser:str = payload.get("user_id")

        if idOfUser is None:
            raise credentials_exception
        
        print(idOfUser)
        
        token_data = schema.TokenData(id=idOfUser)

        print(token_data.id)

        return token_data
   
    except JWTError:
       raise credentials_exception
   

       
# to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token_user = verify_access_token(token, credentials_exception)

    
    user = db.query(models.User).filter(models.User.id == token_user.id).first()


    return user
    # start from 131