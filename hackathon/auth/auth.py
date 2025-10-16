from fastapi import APIRouter,Depends,HTTPException
from hackathon.database import users_collection
from hackathon.schemas.users_schemas import UserCreate,UserLogin
from hackathon.hashing import hash_password,verify_password,pwd_context
from pymongo import MongoClient
from hackathon.auth.token import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register_user(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_pwd
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"user_id": str(user["_id"]), "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}