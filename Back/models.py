from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str 
    email: EmailStr 
    password: str
    confirm_password: str
    role:str='user'


class login(BaseModel):
    email:EmailStr
    password:str


class Shipment(BaseModel):
    ShipmentNumber: str
    RouteDetails : str
    Device: str
    PoNumber: str
    NdcNumber: str
    SerialNumber: str
    ContainerNum: str
    GoodsType: str
    ExpectedDeliveryDate: str
    DeliveryNumber: str
    BatchId: str
    ShipmentDescription: str

class forgotpassword(BaseModel):
    email:EmailStr

class VerifyOtpRequest(BaseModel):
    otp: str

class resetpassword(BaseModel):
    token:str
    newpassword:str
    confirmpassword:str

class DeviceData(BaseModel):
    Battery_Level: float
    Device_ID: str
    First_Sensor_temperature: float
    Route_From: str
    Route_To: str