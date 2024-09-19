from sqlalchemy import TIMESTAMP, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")
                      ,nullable=False)
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text('now()'))

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE", primary_key=True))
    
    movie_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE", primary_key=True))
