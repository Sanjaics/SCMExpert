from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Back.Routes import account, shipment, user, device,feedback

app = FastAPI()

# CORS middleware configuration
origins = ["http://127.0.0.1:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(account.router)
app.include_router(shipment.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(feedback.router)