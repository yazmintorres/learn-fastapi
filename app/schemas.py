from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime

# schema/pydantic model, shape/structure of the request
class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True 

# inherits all the fields from PostBase
class PostCreate(PostBase):
    pass 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]

# RESPONSE MODELS
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # to convert from ORM response object to Pydantic model
    class Config: 
        from_orm = True
        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #to convert from ORM object to Pydantic model
    class Config: 
        from_orm = True

class PostOut(BaseModel):
    post: Post
    votes: int

    #to convert from ORM object to Pydantic model
    class Config: 
        from_orm = True
