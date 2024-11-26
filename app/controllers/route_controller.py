from typing import Tuple

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_async_session
from backend.app.services.route_builder import RouteBuilder
from backend.app.services.traffic_data_service import GoogleAPIConnector

router = APIRouter()


@router.post("/routes")
async def get_routes(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    db_session: AsyncSession = Depends(get_async_session)
):
    try:
        traffic_api_connector = GoogleAPIConnector()
        route_builder = RouteBuilder(traffic_api_connector)
        routes = await route_builder.build_routes(origin, destination, db_session)
        return {"status": "success", "routes": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
