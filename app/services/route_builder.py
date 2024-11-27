import asyncio
from typing import Tuple, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.route_model import save_route_to_db, save_segment_to_db
from ..services.traffic_data_service import TrafficAPIConnector
from ..services.utils import decode_polyline, Coordinates

HIGH_TRAFFIC_THRESHOLD = 1.7
MEDIUM_TRAFFIC_THRESHOLD = 1.4
TRAFFIC_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green",
    "default": "blue"
}

class RouteBuilder:

    def __init__(self, api_connector: TrafficAPIConnector):
        self.api_connector = api_connector

    async def build_routes(self, origin: Coordinates, destination: Coordinates, db_session: AsyncSession) -> List[Dict]:
        origin_str = f"{origin.lat},{origin.lng}"
        destination_str = f"{destination.lat},{destination.lng}"

        routes = await self.api_connector.get_routes(origin_str, destination_str)
        processed_routes = []
        for route in routes:
            route_segments = []
            for leg in route["legs"]:
                await save_route_to_db(leg, db_session)
                route_segments = await self.prepare_segments(leg["steps"], db_session)

            processed_routes.append({
                "summary": route["summary"],
                "distance": route["legs"][0]["distance"]["text"],
                "duration": route["legs"][0]["duration_in_traffic"]["text"],
                "segments": route_segments
            })

        return processed_routes

    async def prepare_segments(self, steps: List[Dict], db_session: AsyncSession) -> List[Dict]:
        async def fetch_traffic_data(step: Dict):
            start_location = f'{step["start_location"]["lat"]},{step["start_location"]["lng"]}'
            end_location = f'{step["end_location"]["lat"]},{step["end_location"]["lng"]}'
            return await self.api_connector.get_segment_traffic(start_location, end_location)

        traffic_data_list = await asyncio.gather(*[fetch_traffic_data(step) for step in steps])

        route_segments = []
        for step, traffic_data in zip(steps, traffic_data_list):

            duration_in_traffic = traffic_data["duration_in_traffic"]["value"]
            normal_duration = traffic_data["duration"]["value"]

            color = self.determine_traffic_color(normal_duration, duration_in_traffic)

            polyline = decode_polyline(step["polyline"]["points"])

            segment = {
                "start_location": step["start_location"],
                "end_location": step["end_location"],
                "duration_in_traffic": duration_in_traffic,
                "normal_duration": normal_duration,
                "polyline": step["polyline"]["points"]
            }
            await save_segment_to_db(segment, db_session)
            route_segments.append({"polyline": polyline, "color": color})

        return route_segments

    def determine_traffic_color(self, normal_duration: int, duration_in_traffic: int) -> str:
        if normal_duration > 0:
            traffic_ratio = duration_in_traffic / normal_duration
            if traffic_ratio > HIGH_TRAFFIC_THRESHOLD:
                return TRAFFIC_COLORS["high"]
            elif MEDIUM_TRAFFIC_THRESHOLD <= traffic_ratio <= HIGH_TRAFFIC_THRESHOLD:
                return TRAFFIC_COLORS["medium"]
            else:
                return TRAFFIC_COLORS["low"]
        return TRAFFIC_COLORS["default"]
