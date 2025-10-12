from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HackathonBase(BaseModel):
    name :str
    tagline :Optional[str]=None
    description: Optional[str]=None
    start_date : datetime
    end_date:datetime
    mode:str
    visibility:str="public"

class HackathonCreate(BaseModel):
    organizer_id:str

class HackathonResponse(BaseModel):
    organizer_id:str
    id:str
    created_at:datetime

    class Config:
        orm_mode:True

        