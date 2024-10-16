from typing import List
from datetime import datetime, timezone, timedelta

import bcrypt, jwt
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import settings
from config.db import user_collection
from models.user import UserModel, UserLoginModel

router = APIRouter(tags=["Auth"], prefix="/auth")

users:List[UserModel] = []

def get_user(user):
    return {
        "_id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"]
    }

@router.get("/profile")
async def profile(request: Request):
    print(request)
    return {"_id": request.state._id}

@router.post("/login")
async def login(user: UserLoginModel):
    is_user = await user_collection.find_one({"email": user.email})
    if not is_user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_user["email"] == user.email and bcrypt.checkpw(user.password.encode("utf-8"), is_user["password"].encode("utf-8")):
        is_user = get_user(is_user)
        token = jwt.encode({"_id": is_user["_id"], "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=86400)}, settings.JWT_SECRET, algorithm="HS256")
        return {"user": is_user, "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
async def register(user: UserModel):
    is_user = await user_collection.find_one({"email": user.email})
    if is_user:
        raise HTTPException(status_code=409, detail="User already exists")
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(8)).decode("utf-8")
    user = jsonable_encoder(user)
    result = await user_collection.insert_one(user)
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    new_user = get_user(new_user)
    token = jwt.encode({"_id": new_user["_id"], "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=86400)}, settings.JWT_SECRET, algorithm="HS256")
    return JSONResponse({"user": new_user, "token": token}, status_code=201)