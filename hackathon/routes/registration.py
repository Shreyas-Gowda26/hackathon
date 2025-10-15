from fastapi import APIRouter,Depends,HTTPException,status
from database import registrations_collection
from schemas.registrations_schemas import Registration_base,Registration_Response
from bson import ObjectId
from typing import List
from datetime import datetime
from hackathon.auth.roles import allow_roles
router=APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)

@router.post("/",response_model=Registration_Response,dependencies=[Depends(allow_roles("participant","admin"))])
def create_Registration(registration:Registration_base):
    registration_dict = registration.model_dump()
    res = registrations_collection.insert_one(registration_dict)
    registration_dict["id"]=str(res.inserted_id)
    registration_dict["created_at"] = datetime.utcnow()
    return Registration_Response(id=str(res.inserted_id),**registration_dict)

@router.get("/{hackathon_id}",response_model=List[Registration_Response])
def get_all_registration_by_hackathon(hackathon_id:str):
    registrations=[]
    for registration in registrations_collection.find(hackathon_id={"$eq":hackathon_id}):
        data={k: registration[k] for k in registration if k!="_id"}
        registrations.append(Registration_Response(id=str(registration["id"]),**data))
    return registrations

@router.get("user/{user_id}",response_model=Registration_Response)
def get_registration_by_user_id(user_id:str):
    registration = registrations_collection.find_one({"user_id":ObjectId(user_id)})
    if not registration: 
        raise HTTPException(status_code=404,detail="Registration not found")
    data = {k: registration[k] for k in registration if k!="_id"}
    return Registration_Response(id=str(registration["_id"]),**data)

