import requests
from backend.app.config import Config


class GoogleAPIConnector:

    BASE_URL = Config.GOOGLE_BASE_URL

    @staticmethod
    async def get_routes(origin: str, destination: str, alternatives: bool = True, departure_time: str = "now"):
        params = {
            "origin": origin,
            "destination": destination,
            "alternatives": "true" if alternatives else "false",
            "key": Config.GOOGLE_MAPS_API_KEY,
            "departure_time": departure_time,
        }

        response = requests.get(GoogleAPIConnector.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"Error from Google Maps API: {data['status']}")

        return data["routes"]

    @staticmethod
    async def get_segment_traffic(start_location: str, end_location: str, departure_time: str = "now"):
        params = {
            "origin": start_location,
            "destination": end_location,
            "key": Config.GOOGLE_MAPS_API_KEY,
            "departure_time": departure_time,
        }

        response = requests.get(GoogleAPIConnector.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"Error from Google Maps API: {data['status']}")

        return data["routes"][0]["legs"][0]
