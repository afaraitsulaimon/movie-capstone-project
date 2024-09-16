from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class MovieBase(BaseModel):
    name: str
    year: int
    description: str

class Movie(MovieBase):
    id: int

class CreateMovie(MovieBase):
    pass

class UpdateMovie(MovieBase):
    pass

# user schema
class UserCreate(BaseModel):
    full_name: str
    address: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # description: str

    class Config:
        orm_mode = True

# for user log in
class UserLogin(BaseModel):
    email:EmailStr
    password: str

# for access token
class Token(BaseModel):
    access_token: str
    token_type: str

# token type
class TokenData(BaseModel):
    id: Optional[int] = None

# schema for what you want to return back to 
# user when viewing Movie
# class MovieView(BaseModel):
#     name: str
#     year: int
#     description: str
#     created_at: datetime
#     owner_id: int

#     class Config:
#         orm_mode = True