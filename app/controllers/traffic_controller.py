from fastapi import APIRouter

router = APIRouter()

@router.get("/traffic")
async def get_traffic():
    return {"message": "Traffic data"}
