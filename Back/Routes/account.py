from fastapi import APIRouter, Depends, HTTPException, Request,status
from typing import List
from Back.auth import get_current_user
from Back.db import users
from fastapi.responses import JSONResponse
from Back.models import UserCreate

router = APIRouter()

@router.get("/myaccount", response_model=dict)
async def myaccount(request: Request, current_user: dict = Depends(get_current_user)):
    try:
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        # Fetch user account data from the database
        user_data = users.find_one({"email": current_user["email"]}, {"_id": 0})

        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Ensure that the necessary fields are present in the user data
        if "username" not in user_data or "email" not in user_data or "role" not in user_data:
            raise HTTPException(status_code=500, detail="User data is incomplete")

        # Extract username, email, role from the user data
        user = {
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        }
        return user
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "detail": str(e)})
