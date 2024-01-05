from fastapi import APIRouter, Depends, HTTPException,status,Request,Response
from fastapi.security import OAuth2PasswordRequestForm
from Back.auth import get_current_user, create_access_token, Hashpass, decode_token, oauth2_scheme
from fastapi.responses import JSONResponse,RedirectResponse
from Back.db import users
from Back.models import UserCreate,forgotpassword
from fastapi.responses import JSONResponse




router = APIRouter()

#signup post router function
@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    try:
        #check user is already exist
        existing_user = users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Password validation
        if (
            len(user.password) < 8
            or not any(char.isdigit() for char in user.password)
            or not any(char.isupper() for char in user.password)
            or not any(char.islower() for char in user.password)
            or not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in user.password)
        ):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long ,1 uppercase,1 lowercase , 1 digit,1 special character."
            )

        hashed_password = Hashpass.create_user(user.password)
        new_user = {"email": user.email, "username": user.username, "password": hashed_password,
                    "role":user.role}
        users.insert_one(new_user)

        return {"message": "Email Registered Successfully"} 
    
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        # Print or log the details of the exception
        print(f"Error in signup: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )


#signin post router function
@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = users.find_one({"email": form_data.username})

        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        if not Hashpass.verify_password(form_data.password, user["password"]):
            raise HTTPException(status_code=400, detail="Incorrect Password")

        login_user = {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
        #create access token after successfull login
        token = create_access_token(data={"sub": user["username"], "email": user["email"],"role" : user["role"]})
        response = JSONResponse(content={"message": "Signin successful","token":token ,"role":login_user["role"], "username": login_user["username"], "email": login_user["email"]})
        return response

    except HTTPException as http_error:
        if http_error.detail == "User not found":
            raise HTTPException(
                status_code=400, detail=http_error.detail)
        if http_error.detail == "Incorrect Password":
            raise HTTPException(
                status_code=400, detail=http_error.detail)
        raise http_error  
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


#forgotpassword post router function
@router.post("/forgotpassword", response_class=JSONResponse)
async def reset_password(user_forgot_password: forgotpassword):
    try:
        user = users.find_one({"email": user_forgot_password.email})

        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        if user_forgot_password.new_password != user_forgot_password.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Password validation
        if (
            len(user_forgot_password.new_password) < 8
            or not any(char.isdigit() for char in user_forgot_password.new_password)
            or not any(char.isupper() for char in user_forgot_password.new_password)
            or not any(char.islower() for char in user_forgot_password.new_password)
            or not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in user_forgot_password.new_password)
        ):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long,one uppercase letter, one lowercase letter, one digit, and one special character."
            )

        hashed_password = Hashpass.create_user(user_forgot_password.new_password)

        # Update the user's password in the database
        result = users.update_one(
            {"email": user_forgot_password.email},
            {"$set": {"password": hashed_password}}
        )

        response_data = {"message": "Password reset successful"}
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        )

#check_authentication get router function
@router.get("/check_authentication", response_model=dict)
async def check_authentication(current_user: dict = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "User is authenticated"}




