from fastapi import APIRouter,Depends,HTTPException
from database import users_collection
from hackathon.schemas.users_schemas import UserBase,UserResponse,UserLogin,UserCreate
from typing import List
from bson import ObjectId
from hackathon.hashing import hash_password
from hackathon.auth.oauth2 import get_current_user
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",response_model=UserResponse)
async def create_user(user:UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    res = users_collection.insert_one(user_dict)
    user_dict["_id"] = str(res.inserted_id)
    return UserResponse(id=str(res.inserted_id), **user_dict)

@router.get("/",response_model=List[UserResponse])
def get_all_users(current_user: UserResponse = Depends(get_current_user)):
    users=[]
    for user in users_collection.find():
        data={k:user[k] for k in user if k!="_id"}
        users.append(UserResponse(id=str(user["_id"]),**data))
    return users

