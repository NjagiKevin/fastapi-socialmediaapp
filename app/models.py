from operator import imod
import sqlalchemy
from .database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



# Post class defines the structure of the posts table
class Post(Base):
    __tablename__= "posts"

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default='TRUE', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #relationship
    owner=relationship("User") 


# User class defines the structure of the users table
class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    password2=Column(String, nullable=False)


# User class defines the structure of the votes table
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



