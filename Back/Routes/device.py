from fastapi import APIRouter, Depends, HTTPException, Request,status
from typing import List
from Back.auth import get_current_user
from Back.db import Device_data
from fastapi.responses import JSONResponse
from Back.models import DeviceData


router = APIRouter()


@router.get("/devicedata", response_model=List[DeviceData])
async def devicedata(request: Request, exist_user: dict = Depends(get_current_user)):
    try:
        if exist_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        elif exist_user['role'] != 'admin':
            raise HTTPException(status_code=401, detail="Admins only Authorised")
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
