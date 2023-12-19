from fastapi import FastAPI, Depends, HTTPException, Request,status
from fastapi.security import OAuth2PasswordRequestForm
import secrets
from starlette import status
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from Back.auth import get_current_user, create_access_token, Hash,decode_token,oauth2_scheme
from Back.db import users, shipment_detail,Device_data
from Back.models import UserCreate, Shipment,forgotpassword,resetpassword,DeviceData
from Back.mail import send_verification_email,generate_otp
import json
from fastapi.responses import JSONResponse,RedirectResponse
from pymongo.cursor import Cursor
import datetime
from typing import List
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

from fastapi import FastAPI



OTP_EXPIRATION_MINUTES = 5
TOKEN_EXPIRATION_MINUTES = 30



# CORS middleware configuration
origins = ["http://127.0.0.1:5500"]  # Add the origins of your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/check_authentication", response_model=dict)
async def check_authentication(current_user: dict = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "User is authenticated"}

@app.get("/dashboard", response_model=dict)
async def get_dashboard(request: Request, exist_user: dict = Depends(get_current_user)):
    if exist_user is None:
        return RedirectResponse(url="/index.html")

@app.post("/signup", response_model=dict)
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
                detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
            )

        hashed_password = Hash.create_user(user.password)
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



@app.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = users.find_one({"email": form_data.username})

        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        if not Hash.verify_password(form_data.password, user["password"]):
            raise HTTPException(status_code=400, detail="Incorrect Password")

        login_user = {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
        
        #create access token after successfull login
        token = create_access_token(data={"sub": user["username"], "email": user["email"]})
        print(token)
        response = JSONResponse(content={"message": "Signin successful","token":token })
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

                             
@app.post("/Create_shipment", response_model=dict)
async def shipment(request: Request, ship:Shipment,exist_user: dict = Depends(get_current_user)):
        print("user_exist",exist_user)
        if exist_user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

            # Check if the shipment is already registered
        existing_shipment = shipment_detail.find_one({"ShipmentNumber": ship.ShipmentNumber})

        if existing_shipment:
                raise HTTPException(status_code=400, detail="Shipment already exists")
        # print("pythoncode")
        NewShipment_data = {
            "username": exist_user["username"],
            "email": exist_user["email"],  
            "ShipmentNumber":ship.ShipmentNumber,
            "RouteDetails":ship.RouteDetails,
            "Device": ship.Device,
            "PoNumber": ship.PoNumber,
            "NdcNumber": ship.NdcNumber,
            "SerialNumber": ship.SerialNumber,
            "ContainerNum": ship.ContainerNum,
            "GoodsType": ship.GoodsType,
            "ExpectedDeliveryDate": ship.ExpectedDeliveryDate,
            "DeliveryNumber": ship.DeliveryNumber,
            "BatchId": ship.BatchId,
            "ShipmentDescription":ship.ShipmentDescription}


        # Ensure that NewShipment_data is converted to a dictionary before insertion
        shipment_detail.insert_one(NewShipment_data)
        print(NewShipment_data)

        return {"message": "Shipment added successfully"}




@app.get("/myshipment", response_model=list)
async def myshipment(request: Request, exist_user: dict = Depends(get_current_user)):
    try:
        if exist_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        elif exist_user['role'] == 'admin':
            All_exist_shipments = list(shipment_detail.find())
            for shipment in All_exist_shipments:
                shipment['_id'] = str(shipment['_id'])
            return JSONResponse(content=All_exist_shipments)
        
        exist_shipments = list(shipment_detail.find({"username":exist_user["username"] },{"_id":0}))
        return JSONResponse(content=exist_shipments)
        
    except HTTPException as http_error:
        if http_error.detail == "Not authenticated":
            raise HTTPException(status_code=400, detail=http_error.detail)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/forgotpassword", response_model=dict)
async def forgot_password(forgot_data: forgotpassword):
    try:
        user = users.find_one({'email': forgot_data.email})

        if user:
            # Check if an OTP has been generated recently
            if user.get("otp_timestamp") and (datetime.datetime.utcnow() - user["otp_timestamp"]).total_seconds() / 60 < OTP_EXPIRATION_MINUTES:
                raise HTTPException(status_code=400, detail="OTP already sent. Please wait before requesting a new one.")

            # Generate an OTP
            otp = generate_otp()

            # Send the OTP email 
            send_verification_email("rsanjai@exafluence.com", otp, forgot_data.email)

            # Return a response
            return {"message": "OTP sent to your email"}
        else:
            raise HTTPException(status_code=400, detail="Email id not registered")
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@app.post("/verifyotp", response_model=dict)
async def verify_otp(otp: str, token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token to get the user's email
        payload = decode_token(token)
        if payload and "sub" in payload:
            email = payload["sub"]

            # Check if the provided OTP matches the one stored in the database
            user = users.find_one({'email': email})
            if user and user.get("otp") == otp:
                # Validate OTP expiration (adjust as needed)
                if user.get("otp_timestamp") and (datetime.utcnow() - user["otp_timestamp"]).total_seconds() / 60 < OTP_EXPIRATION_MINUTES:
                    # Clear the OTP after successful verification
                    users.update_one({"email": email})
                    return {"message": "OTP verified successfully", "success": True}
                else:
                    raise HTTPException(status_code=400, detail="Invalid or expired OTP")
            else:
                raise HTTPException(status_code=400, detail="Invalid OTP")
        else:
            raise HTTPException(status_code=400, detail="Invalid token")
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )

@app.post("/resetpassword", response_model=dict)
async def reset_password(new_password: str, confirm_password: str, token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token to get the user's email
        payload = decode_token(token)
        if payload and "sub" in payload:
            email = payload["sub"]

            # Check if the new password and confirm password match
            if new_password == confirm_password:
                # Update the user's password in the database
                hashed_password = Hash.create_user(new_password)
                users.update_one({"email": email}, {"$set": {"password": hashed_password}})
                return {"message": "Password reset successfully"}
            else:
                raise HTTPException(status_code=400, detail="New password and confirm password do not match")
        else:
            raise HTTPException(status_code=400, detail="Invalid token")
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )



@app.get("/devicedata", response_model=List[DeviceData])
async def devicedata(request: Request, exist_user: dict = Depends(get_current_user)):
    try:
        if exist_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        elif exist_user['role'] != 'admin':
            raise HTTPException(status_code=401, detail="Admins only Authorised")
        # print(exist_user)
        device_streamdata = list(Device_data.find({}, {"_id": 0}))

        if not device_streamdata:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No device data found")

        # Convert 'Device_ID' to string in each record
        for record in device_streamdata:
            record['Device_ID'] = str(record['Device_ID'])

        return device_streamdata
    except HTTPException as http_error:
        if http_error.detail == "Not authenticated":
            raise HTTPException(status_code=400, detail=http_error.detail)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")





@app.get("/myaccount", response_model=dict)
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


# @app.get("/favicon.ico")
# async def get_favicon():
#     return FileResponse("favicon.ico")



# @app.get("/myshipment", response_model=List[dict])  # Change response_model to List[dict]
# async def get_myshipment(exist_user: dict = Depends(get_current_user)):
#     if exist_user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

#     # Retrieve shipment details from the database based on shipment number
#     shipment_cursor: Cursor = shipment_detail.find({"_id": 0})
    
#     # Convert cursor to list of dictionaries
#     shipment_data = list(shipment_cursor)
    
#     print(shipment_data)

#     return shipment_data