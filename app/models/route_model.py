from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from backend.app.models import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    start_address = Column(String, nullable=False)
    start_lat = Column(Float, nullable=False)
    start_lng = Column(Float, nullable=False)
    end_address = Column(String, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lng = Column(Float, nullable=False)
    distance_text = Column(String, nullable=False)
    distance_value = Column(Integer, nullable=False)
    duration_text = Column(String, nullable=False)
    duration_value = Column(Integer, nullable=False)
    duration_in_traffic_text = Column(String, nullable=True)
    duration_in_traffic_value = Column(Integer, nullable=True)


class RouteSegment(Base):
    __tablename__ = "route_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_lat = Column(Float, nullable=False)
    start_lng = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lng = Column(Float, nullable=False)
    duration_in_traffic = Column(Integer, nullable=False)
    normal_duration = Column(Integer, nullable=False)
    polyline = Column(String, nullable=False)


async def save_route_to_db(route_data: dict, db_session: AsyncSession):
    route = Route(
            start_address=route_data.get("start_address"),
            start_lat=route_data["start_location"]["lat"],
            start_lng=route_data["start_location"]["lng"],
            end_address=route_data.get("end_address"),
            end_lat=route_data["end_location"]["lat"],
            end_lng=route_data["end_location"]["lng"],
            distance_text=route_data["distance"]["text"],
            distance_value=route_data["distance"]["value"],
            duration_text=route_data["duration"]["text"],
            duration_value=route_data["duration"]["value"],
            duration_in_traffic_text=route_data.get("duration_in_traffic", {}).get("text"),
            duration_in_traffic_value=route_data.get("duration_in_traffic", {}).get("value"),
    )

    db_session.add(route)
    await db_session.commit()
    await db_session.refresh(route)


async def save_segment_to_db(segment: list, db_session: AsyncSession):
    route_segment = RouteSegment(
        start_lat=segment["start_location"]["lat"],
        start_lng=segment["start_location"]["lng"],
        end_lat=segment["end_location"]["lat"],
        end_lng=segment["end_location"]["lng"],
        duration_in_traffic=segment["duration_in_traffic"],
        normal_duration=segment["normal_duration"],
        polyline=segment["polyline"],
    )
    db_session.add(route_segment)
    await db_session.commit()
