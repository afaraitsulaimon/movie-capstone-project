from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
import database
from model import models
from database import get_db
import oauth2
import schema
import utils


ratingRouter = APIRouter(
    prefix="/rating",
    tags=['Ratings']
    )

# route for rating a movie
@ratingRouter.post("/", status_code=status.HTTP_201_CREATED)
def rating_movie(rate: schema.Rate, db: Session = Depends(database.get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # fetch the data inside the rating
    rating_query = db.query(models.Rating).filter(
        models.Rating.movie_id == rate.movie_id, models.Rating.user_id == current_user.id
    )

    founded_rating = rating_query.first()

    print(founded_rating)
    # if the rating and the user id is fetched at the same time
    # then delete it from the rating
    if (rate.dir == 1):
        if founded_rating:
            # founded_rating.delete(synchronize_session=False)
            db.delete(founded_rating)
            db.commit()

            return {"message":"Rating Successfully remove"}
        
        # if the rating and user id is not found
        # then add new rating
        if not founded_rating:
            add_rating = models.Rating(user_id = current_user.id, movie_id = rate.movie_id)
            db.add(add_rating)
            db.commit()

            return {"message":"Successfully Rated"}
        


    # start from 157