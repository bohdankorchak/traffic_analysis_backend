from fastapi import APIRouter

router = APIRouter()

@router.post("/route")
async def create_route():
    return {"message": "Route created"}
