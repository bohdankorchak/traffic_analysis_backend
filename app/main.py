from fastapi import FastAPI
from app.controllers import traffic_controller, route_controller

app = FastAPI()

app.include_router(traffic_controller.router)
app.include_router(route_controller.router)

@app.get("/")
async def root():
    return {"message": "City Traffic Analysis System"}
