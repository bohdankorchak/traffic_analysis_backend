# Тест test_get_routes_success:
#
# Перевіряє, чи правильно працює метод get_routes, коли API повертає успішну відповідь.
# Тест test_get_routes_error:
#
# Перевіряє, чи метод викликає ValueError, якщо статус відповіді API не "OK".
# Тест test_get_segment_traffic_success:
#
# Перевіряє метод get_segment_traffic, коли API повертає успішну відповідь.
# Тест test_get_segment_traffic_error:
#
# Перевіряє, чи метод get_segment_traffic викликає ValueError, якщо статус відповіді API не "OK".

import unittest
from unittest.mock import patch, MagicMock

from backend.app.config import Config
from backend.app.services.traffic_data_service import GoogleAPIConnector


class TestGoogleAPIConnector(unittest.TestCase):

    @patch("backend.app.services.traffic_data_service.requests.get")
    async def test_get_routes_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "routes": [
                {"summary": "Route 1", "legs": []},
                {"summary": "Route 2", "legs": []},
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Виклик методу
        origin = "50.4501,30.5234"
        destination = "50.4519,30.5223"
        result = await GoogleAPIConnector.get_routes(origin, destination)

        # Перевірка
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["summary"], "Route 1")
        self.assertEqual(result[1]["summary"], "Route 2")
        mock_get.assert_called_once_with(
            GoogleAPIConnector.BASE_URL,
            params={
                "origin": origin,
                "destination": destination,
                "alternatives": "true",
                "key": Config.GOOGLE_MAPS_API_KEY,
                "departure_time": "now",
            },
        )

    @patch("backend.app.services.traffic_data_service.get")
    async def test_get_routes_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "INVALID_REQUEST"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        origin = "50.4501,30.5234"
        destination = "50.4519,30.5223"

        # Перевірка, що викликається ValueError
        with self.assertRaises(ValueError) as context:
            await GoogleAPIConnector.get_routes(origin, destination)

        self.assertEqual(
            str(context.exception), "Error from Google Maps API: INVALID_REQUEST"
        )

    @patch("backend.app.services.traffic_data_service.requests.get")
    async def test_get_segment_traffic_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "routes": [
                {
                    "legs": [
                        {
                            "start_address": "Start Point",
                            "end_address": "End Point",
                            "duration": {"value": 600, "text": "10 mins"},
                            "distance": {"value": 5000, "text": "5 km"},
                        }
                    ]
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Виклик методу
        start_location = "50.4501,30.5234"
        end_location = "50.4519,30.5223"
        result = await GoogleAPIConnector.get_segment_traffic(start_location, end_location)

        # Перевірка
        self.assertEqual(result["duration"]["text"], "10 mins")
        self.assertEqual(result["distance"]["text"], "5 km")
        mock_get.assert_called_once_with(
            GoogleAPIConnector.BASE_URL,
            params={
                "origin": start_location,
                "destination": end_location,
                "key": Config.GOOGLE_MAPS_API_KEY,
                "departure_time": "now",
            },
        )

    @patch("backend.app.services.traffic_data_service.requests.get")
    async def test_get_segment_traffic_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "INVALID_REQUEST"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        start_location = "50.4501,30.5234"
        end_location = "50.4519,30.5223"

        # Перевірка, що викликається ValueError
        with self.assertRaises(ValueError) as context:
            await GoogleAPIConnector.get_segment_traffic(start_location, end_location)

        self.assertEqual(
            str(context.exception), "Error from Google Maps API: INVALID_REQUEST"
        )