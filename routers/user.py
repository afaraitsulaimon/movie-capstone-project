from fastapi import APIRouter, Depends, HTTPException, Response, status
from schema import UserCreate, UserOut
from sqlalchemy.orm import Session
from model import models
from database import get_db
import utils


userRouter = APIRouter(
    prefix="/users",
    tags=['Users']
    )


# route for user registration

@userRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(createuser: UserCreate, db: Session = Depends(get_db)):
    # let's hash the password fits before 
    # passing it to the database

    hashed_pw = utils.hash(createuser.password)

    # restore the password passed by the client as the hashed password
    createuser.password = hashed_pw
    
    new_user = models.User(**createuser.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#  get user by id
@userRouter.get('/{id}', response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    # run a query to fetch the user

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"User  with id : {id} not found")
    
    return user
        