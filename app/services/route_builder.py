from typing import Tuple, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.route_model import save_route_to_db, save_segment_to_db
from backend.app.services.traffic_data_service import TrafficAPIConnector
from backend.app.services.utils import decode_polyline


class RouteBuilder:

    def __init__(self, api_connector: TrafficAPIConnector):
        self.api_connector = api_connector

    async def build_routes(self, origin: Tuple[float, float], destination: Tuple[float, float], db_session: AsyncSession) -> List[Dict]:
        origin_str = f"{origin[0]},{origin[1]}"
        destination_str = f"{destination[0]},{destination[1]}"

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
        route_segments = []
        for step in steps:
            start_location = f'{step["start_location"]["lat"]},{step["start_location"]["lng"]}'
            end_location = f'{step["end_location"]["lat"]},{step["end_location"]["lng"]}'

            traffic_data = await self.api_connector.get_segment_traffic(start_location, end_location)

            duration_in_traffic = traffic_data["duration_in_traffic"]["value"]
            normal_duration = traffic_data["duration"]["value"]
            if normal_duration > 0:
                traffic_ratio = duration_in_traffic / normal_duration
                if traffic_ratio > 1.45:
                    color = "red"
                elif 1.3 <= traffic_ratio <= 1.45:
                    color = "yellow"
                else:
                    color = "green"
            else:
                color = "blue"

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
