from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from hackathon.schemas.registrations_schemas import Registration_base,Registration_Response
from bson import ObjectId
from typing import List
from datetime import datetime
from hackathon.auth.roles import allow_roles
from hackathon.database import users_collection,registrations_collection,hackathon_collection
from hackathon.notification.email_utils import send_email
router=APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)

@router.post("/", response_model=Registration_Response, dependencies=[Depends(allow_roles("participant", "admin"))])
async def create_registration(registration: Registration_base, background_tasks: BackgroundTasks):
    # ✅ Check if user and hackathon exist
    hackathon = hackathon_collection.find_one({"_id": ObjectId(registration.hackathon_id)})
    user = users_collection.find_one({"_id": ObjectId(registration.user_id)})

    if not hackathon or not user:
        raise HTTPException(status_code=404, detail="User or Hackathon not found")

    # ✅ Prevent duplicate registrations
    existing = registrations_collection.find_one({
        "hackathon_id": registration.hackathon_id,
        "user_id": registration.user_id
    })
    if existing:
        raise HTTPException(status_code=400, detail="User already registered for this hackathon")

    # ✅ Create registration record
    registration_dict = registration.model_dump()
    registration_dict["registered_at"] = datetime.utcnow()
    res = registrations_collection.insert_one(registration_dict)

    # ✅ Send email in background
    background_tasks.add_task(
        send_email,
        subject=f"🎉 Registered for {hackathon.get('name', 'Hackathon')}",
        recipients=[user["email"]],
        body=f"""
        <h3>Hey {user['name']}!</h3>
        <p>You have successfully registered for <b>{hackathon.get('name')}</b>.</p>
        <p>We can’t wait to see your amazing project!</p>
        """
    )

    return Registration_Response(
        id=str(res.inserted_id),
        registered_at=registration_dict["registered_at"]
    )

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

