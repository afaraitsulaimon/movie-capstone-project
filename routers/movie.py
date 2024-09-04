from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
import oauth2
from schema import CreateMovie, UpdateMovie
from sqlalchemy.orm import Session
from model import models
from database import get_db



movieRouter = APIRouter(
    prefix="/movies",
    tags=['Movies']
    )


@movieRouter.get("/")
def get_movie(db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    all_movies = db.query(models.Movie).all()
    return {"message":"Movies retrieved", "data":all_movies}


# create a new movie
@movieRouter.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(new_movie: CreateMovie, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    theNewMovie = models.Movie(
        name=new_movie.name, 
        year=new_movie.year,
        description=new_movie.description
        # **new_movie.model_dump()
    )

    db.add(theNewMovie)
    db.commit()
    db.refresh(theNewMovie)

    return{"data":theNewMovie}


    # start from page 69

# fetch single movie
@movieRouter.get("/{id}")
def get_single_movie(id: int, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):

    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    
    # check if the movie is not available return exception message
    if not movie:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"movie with id : {id} not found")
    
    # if found , return the below
    return{"message":"Movie Successfully retrieved", "data": movie}
    


# delete a post
@movieRouter.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # fetch the post and compare with the passed 

    themovie = db.query(models.Movie).filter(models.Movie.id == id)

    # check if the one fetched is not available, return error message
    if not themovie.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             details=f"Movie with id: {id} not found")
    
    # if found then delete what we fetched

    themovie.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a post
@movieRouter.put("/{id}")
def update_movie(id: int, movie_update: UpdateMovie, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # fetch the data of what you want to update first
    movie_query = db.query(models.Movie).filter(models.Movie.id == id)

    movie = movie_query.first()

    # if id is not in the available, raise error
    if not movie:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             details=f"movie with id: {id} not found")
    
    movie_query.update(movie_update.model_dump(), synchronize_session=False)

    db.commit()
    
    return{"message":"Movie successfully Updated", "data": movie_query.first()}
    

