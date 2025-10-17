from fastapi import APIRouter,Depends,HTTPException,status
from database import submissions_collection
from schemas.submission_schemas import SubmissionBase,SubmissionResponse,SubmissionCreate
from typing import List
from datetime import datetime
from bson import ObjectId
router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

@router.post("/",response_model=SubmissionResponse)
def create_submission(submission:SubmissionCreate):
    submission_dict = submission.model_dump()
    res = submissions_collection.insert_one(submission_dict)
    submission_dict["submitted_at"]= datetime.utcnow()
    submission_dict["id"]=str(res.inserted_id)
    return SubmissionResponse(id=str(res.inserted_id),**submission_dict)

@router.get("/{hackathon_id}",response_model=List[SubmissionResponse])
def get_all_submissions(hackathon_id:str):
    submissions=[]
    for submission in submissions_collection.find(hackathon_id={"$eq":hackathon_id}):
        data={k: submission[k] for k in submission if k!="_id"}
        submissions.append(SubmissionResponse(id=str(submission["id"]),**data))
    return submissions

@router.get("/user/{user_id}",response_model=SubmissionResponse)
def get_submission_by_id(user_id:str):
    submission = submissions_collection.find_one({"user_id":ObjectId(user_id)})
    if not submission:
        raise HTTPException(status_code=404,detail="Submission not found")
    data = {k: submission[k] for k in submission if k!="_id"}
    return SubmissionResponse(id=str(submission["_id"]),**data)

