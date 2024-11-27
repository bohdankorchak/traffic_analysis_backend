import requests
from ..config import Config

from typing import List, Tuple, Dict


class TrafficAPIConnector:

    BASE_URL = ""

    async def get_routes(self, origin: str, destination: str, alternatives: bool = True, departure_time: str = "now") -> List[Dict]:
        raise NotImplementedError("This method must be implemented by subclasses.")

    async def get_segment_traffic(self, start_location: str, end_location: str, departure_time: str = "now"):
        raise NotImplementedError("This method must be implemented by subclasses.")


class GoogleAPIConnector(TrafficAPIConnector):

    BASE_URL = Config.GOOGLE_BASE_URL

    async def get_routes(self, origin: str, destination: str, alternatives: bool = True, departure_time: str = "now"):
        params = {
            "origin": origin,
            "destination": destination,
            "alternatives": "true" if alternatives else "false",
            "key": Config.GOOGLE_MAPS_API_KEY,
            "departure_time": departure_time,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"Error from Google Maps API: {data['status']}")

        return data["routes"]

    async def get_segment_traffic(self, start_location: str, end_location: str, departure_time: str = "now"):
        params = {
            "origin": start_location,
            "destination": end_location,
            "key": Config.GOOGLE_MAPS_API_KEY,
            "departure_time": departure_time,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"Error from Google Maps API: {data['status']}")

        return data["routes"][0]["legs"][0]
