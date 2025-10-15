from fastapi import APIRouter,Depends,HTTPException,status
from database import hackathon_collection
from hackathon.schemas.hackathon_schemas import HackathonBase,HackathonResponse
from typing import List
from datetime import datetime
from bson import ObjectId
from hackathon.auth.roles import allow_roles
router = APIRouter(
    prefix="/hackathons",
    tags=["Hackathons"]
)

@router.post("/",response_model=HackathonResponse, dependencies=[Depends(allow_roles("organizer","admin"))])
def create_hackathon(hackathon:HackathonBase):
    hackathon_dict = hackathon.model_dump()
    res = hackathon_collection.insert_one(hackathon_dict)
    hackathon_dict["created_at"]= datetime.utcnow()
    hackathon_dict["id"]=str(res.inserted_id)
    return HackathonResponse(id=str(res.inserted_id),**hackathon_dict)

@router.get("/",response_model=List[HackathonResponse])
def get_all_hackathons():
    hackathons = []
    for hackathon in hackathon_collection.find():
        data = {k : hackathon[k] for k in hackathon if k!="_id"}
        hackathons.append(HackathonResponse(id=str(hackathon["id"]),**data))
    return hackathons

@router.get("/{hackathon_id}",response_model=HackathonResponse)
def get_hackathon_by_id(hackathon_id:str):
    hackathon = hackathon_collection.find_one({"_id":ObjectId(hackathon_id)})
    if not hackathon:
        raise HTTPException(status_code=404,detail="Hackathon not found")
    data = {k: hackathon[k] for k in hackathon if k!="_id"}
    return HackathonResponse(id=str(hackathon["_id"]),**data)

@router.put("/{hackathon_id}",response_model=HackathonResponse)
def update_hackathon(hackathon_id:str,hackathon:HackathonBase):
    existing_hackathon = hackathon_collection.find_one({"_id":ObjectId(hackathon_id)})
    if not existing_hackathon:
        raise HTTPException(status_code =404,detail="Hackathon not found")
    updated_hackathon = hackathon.model_dump()
    hackathon_collection.update_one({"_id":ObjectId(hackathon_id)},{"$set":updated_hackathon})
    updated_hackathon["id"]=hackathon_id
    return HackathonResponse(id=hackathon_id,**updated_hackathon)

@router.delete("/{hackathon_id}",response_model=HackathonResponse)
def delete_hackathon(hackathon_id:str):
    hackathon = hackathon_collection.find_one({"_id":ObjectId(hackathon_id)})
    if not hackathon:
        raise HTTPException(status_code=404,detail="Hackathon not found")
    hackathon_collection.delete_one({"_id":ObjectId(hackathon_id)})
    data={k: hackathon[k] for k in hackathon if k!="_id"}
    return HackathonResponse(id=str(hackathon["_id"]),**data)


