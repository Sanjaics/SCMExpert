
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request,status
from Back.auth import get_current_user
from fastapi.responses import JSONResponse
from Back.models import Shipment
from Back.db import shipment_detail
from dotenv import load_dotenv


load_dotenv()



router = APIRouter()

@router.post("/Create_shipment", response_model=dict)
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




@router.get("/myshipment", response_model=list)
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