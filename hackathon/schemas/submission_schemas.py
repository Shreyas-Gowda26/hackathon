from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubmissionBase(BaseModel):
    hackathon_id:str
    user_id:str
    project_name:str
    description:Optional[str]=None
    github_link:Optional[str]=None
    file_url:Optional[str]=None
    video_link:Optional[str]=None

class SubmissionCreate(SubmissionBase):
    id:str
    submitted_at:datetime

    class Config:
        orm_mode = True