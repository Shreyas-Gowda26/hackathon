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
    file_url: Optional[str] = None
    file_path: Optional[str] = None
    submitted_at: Optional[datetime] = None

    
class SubmissionResponse(SubmissionBase):
    id: str
    file_url: Optional[str] = None
    file_path: Optional[str] = None
    submitted_at: datetime

    class Config:
        orm_mode = True