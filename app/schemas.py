from pydantic import BaseModel,conint
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    content: str
    is_completed: bool = False  # Default value should be assigned like this

class TaskOut(BaseModel):
    id: int
    title: str
    is_completed: Optional[bool]  # Optional should be outside of the list brackets
    owner_name:str


class UserBase(BaseModel):
    username:str
    password:str

class UserCreate(BaseModel):
    username:str
    password:str

class UserUpdate(BaseModel):
    username:str
    password:str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime


class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
     username: str

class postBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(postBase):
    title: str
    content: str
    published: bool = True
    
class PostCreateOut(postBase):
    title: str
    content: str
    published: bool = True
    owner_name:str
    

class PostUpdate(postBase):
    title: str
    content: str
    published: bool = True

class PostOut(BaseModel):
    id:int
    title: str
    content: str
    created_at:datetime
    owner:UserOut

class PostView(BaseModel):
    Post:PostOut
    votes:int
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
