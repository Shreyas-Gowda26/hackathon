from fastapi import APIRouter,HTTPException
from database import scores_collection
from schemas.score_schemas import ScoreBase,ScoreResponse
from typing import List
from datetime import datetime
from bson import ObjectId

router=APIRouter(
    prefix="/scores",
    tags=["scores"]
)

@router.post("/",response_model=ScoreResponse)
def create_score(score:ScoreBase):
    score_dict = score.model_dump()
    res = scores_collection.insert_one(score_dict)
    score_dict["id"]=str(res.inserted_id)
    score_dict["scored_at"]=datetime.utcnow()
    return ScoreResponse(id=str(res.inserted_id),**res)

@router.get("/{hackathon_id}",response_model=List[ScoreResponse])
def get_all_scores_by_hackathon(hackathon_id:str):
    scores =[]
    for score in scores_collection.find(hackathon_id={"$eq":hackathon_id}):
        data={k: score[k] for k in score if k!="_id"}
        scores.append(ScoreResponse(id=str(score["_id"]),**data))
    return scores

@router.get("/submissions/{submission_id}",response_model=List[ScoreResponse])
def get_all_scores_by_submission(submission_id:str):
    scores=[]
    for score in scores_collection.find(submission_id={"$eq":submission_id}):
        data={k: score[k] for k in score if k!="_id"}
        scores.append(ScoreResponse(id=str(score["_id"]),**data))
    return scores