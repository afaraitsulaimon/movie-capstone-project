from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from database import get_db
import oauth2
from schema import UserLogin
from model import models
import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


authRouter = APIRouter(
    tags=["Authentication"]
)

@authRouter.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail= f'User with email: {user_credentials.username} not found' )
    # check if the credentials are wrong
    # throw an error message

    if not utils.verify(user_credentials.password, user.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail= f'Invalid Credentials')
    
    # we called the function verify from inside utils.py (utils.verify)
    # then pass the password client passed and the one fetched from db

    utils.verify(user_credentials.password, user.password)

    access_token = oauth2.create_access_token(data={"user_id" : user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}

