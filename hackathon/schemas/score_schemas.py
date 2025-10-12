from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScoreBase(BaseModel):
    submission_id:str
    judge_id:str
    score:float
    feedback : Optional[str] = None

class ScoreResponse(ScoreBase):
    id : str
    scored_at : datetime

    class Config:
        orm_mode = True