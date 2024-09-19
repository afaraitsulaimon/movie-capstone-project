from fastapi import FastAPI
from routers import movie, user, auth, rating
from  model import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(movie.movieRouter)
app.include_router(user.userRouter)
app.include_router(auth.authRouter)
app.include_router(rating.ratingRouter)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# fetch all movie
