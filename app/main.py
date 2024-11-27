from fastapi import FastAPI

from backend.app.models import init_db
from backend.app.controllers import traffic_controller, route_controller
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замініть на конкретні домени, якщо необхідно
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяє всі методи (GET, POST, PUT тощо)
    allow_headers=["*"],  # Дозволяє всі заголовки
)

app.include_router(traffic_controller.router)
app.include_router(route_controller.router)

@app.get("/")
async def root():
    return {"message": "City Traffic Analysis System"}
