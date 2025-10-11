from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import Optional,List

class UserBase(BaseModel):
    name : str
    email : EmailStr
    role :str = Field(...,pattern="^(organizer|participant|judge|admin)$")

class UserCreate(UserBase):
    password:str

class UserLogin(UserBase):
    email : EmailStr
    password :str

class UserResponse(UserBase):
    id:str
    created_at = datetime

    class Config:
        orm_mode = True