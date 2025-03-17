from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional,Literal

# this is how schema model should request and response

class BasePost(BaseModel):
    title: str
    content: str 
    published:bool=True

class PostCreate(BasePost):
    pass

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode=True
        
class Post(BasePost):
    id: int
    created_at: datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode=True

class CreateUser(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir: Literal[0, 1]