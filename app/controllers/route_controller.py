from typing import Tuple

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_async_session
from backend.app.services.route_builder import RouteBuilder

router = APIRouter()


@router.post("/routes")
async def get_routes(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    db_session: AsyncSession = Depends(get_async_session)
):
    try:
        route_builder = RouteBuilder()
        routes = await route_builder.build_routes(origin, destination, db_session)
        return {"status": "success", "routes": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
