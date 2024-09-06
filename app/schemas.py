from operator import le
from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional, Annotated


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 

    class Config:
        from_attributes = True
    
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# Votes
# Define a type alias for constrained integer
ConstrainedInt = conint(le=1)

class Vote(BaseModel):
    post_id: int
    dir:  Annotated[int, Field(strict=True, le=1)]



