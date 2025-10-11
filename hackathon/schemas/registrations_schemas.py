from pydantic import BaseModel,EmailStr
from datetime import datetime

class Registration_base(BaseModel):
    hackathon_id :str
    user_id:str
    team_name:str

class Registration_Response(BaseModel):
    id:str
    registered_at : datetime

    class Config:
        orm_mode:str

    