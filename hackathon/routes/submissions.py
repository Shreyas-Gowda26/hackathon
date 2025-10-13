from fastapi import APIRouter,Depends,HTTPException,status
from database import submissions_collection
from schemas.submission_schemas import SubmissionBase,SubmissionCreate
from typing import List
from datetime import datetime
from bson import ObjectId
router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

@router.post("/",response_model=SubmissionBase)
def create_submission(submission:SubmissionCreate):
    submission_dict = submission.model_dump()
    res = submissions_collection.insert_one(submission_dict)
    submission_dict["submitted_at"]= datetime.utcnow()
    submission_dict["id"]=str(res.inserted_id)
    return SubmissionBase(id=str(res.inserted_id),**submission_dict)

@router.get("/{hackathon_id}",response_model=List[SubmissionBase])
def get_all_submissions(hackathon_id:str):
    submissions=[]
    for submission in submissions_collection.find(hackathon_id={"$eq":hackathon_id}):
        data={k: submission[k] for k in submission if k!="_id"}
        submissions.append(SubmissionBase(id=str(submission["id"]),**data))
    return submissions

@router.get("/user/{user_id}",response_model=SubmissionBase)
def get_submission_by_id(user_id:str):
    submission = submissions_collection.find_one({"user_id":ObjectId(user_id)})
    if not submission:
        raise HTTPException(status_code=404,detail="Submission not found")
    data = {k: submission[k] for k in submission if k!="_id"}
    return SubmissionBase(id=str(submission["_id"]),**data)

