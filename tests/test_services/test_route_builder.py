# test_build_routes_success:
#
# Перевіряє успішний сценарій, коли маршрути і сегменти обробляються коректно.
# Перевіряє правильність викликів залежностей (save_route_to_db, save_segment_to_db, decode_polyline, get_segment_traffic).
# test_build_routes_error_handling:
#
# Перевіряє сценарій, коли steps у маршруті порожній, і save_segment_to_db не викликається.

import unittest
from unittest.mock import patch, AsyncMock
from backend.app.services.route_builder import RouteBuilder
from backend.app.services.traffic_data_service import GoogleAPIConnector


class TestRouteBuilder(unittest.IsolatedAsyncioTestCase):

    @patch("backend.app.services.route_builder.save_route_to_db", new_callable=AsyncMock)
    @patch("backend.app.services.route_builder.save_segment_to_db", new_callable=AsyncMock)
    @patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_routes", new_callable=AsyncMock)
    @patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_segment_traffic", new_callable=AsyncMock)
    @patch("backend.app.services.route_builder.decode_polyline")
    async def test_build_routes_success(self, mock_decode_polyline, mock_get_segment_traffic, mock_get_routes, mock_save_segment_to_db, mock_save_route_to_db):
        mock_get_routes.return_value = [{"summary": "Route 1", "legs": [{"distance": {"text": "10 km", "value": 10000}, "duration_in_traffic": {"text": "20 mins", "value": 1200}, "duration": {"text": "20 mins", "value": 1200}, "start_location": {"lat": 50.4501, "lng": 30.5234}, "end_location": {"lat": 50.4519, "lng": 30.5223}, "steps": [{"start_location": {"lat": 50.4501, "lng": 30.5234}, "end_location": {"lat": 50.4519, "lng": 30.5223}, "polyline": {"points": "mock_polyline"}}]}]}]
        mock_get_segment_traffic.return_value = {"duration_in_traffic": {"value": 800}, "duration": {"value": 500}}
        mock_decode_polyline.return_value = [(50.4501, 30.5234), (50.4519, 30.5223)]
        route_builder = RouteBuilder(GoogleAPIConnector())
        origin = (50.4501, 30.5234)
        destination = (50.4519, 30.5223)
        db_session = AsyncMock()
        result = await route_builder.build_routes(origin, destination, db_session)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["summary"], "Route 1")
        self.assertEqual(result[0]["distance"], "10 km")
        self.assertEqual(result[0]["duration"], "20 mins")
        self.assertEqual(len(result[0]["segments"]), 1)
        self.assertEqual(result[0]["segments"][0]["color"], "yellow")
        mock_get_routes.assert_called_once_with(
            f"{origin[0]},{origin[1]}", f"{destination[0]},{destination[1]}"
        )
        mock_save_route_to_db.assert_called_once_with(
            mock_get_routes.return_value[0]["legs"][0], db_session
        )
        mock_save_segment_to_db.assert_called_once()
        mock_get_segment_traffic.assert_called_once()
        mock_decode_polyline.assert_called_once_with("mock_polyline")

    @patch("backend.app.services.route_builder.save_route_to_db", new_callable=AsyncMock)
    @patch("backend.app.services.route_builder.save_segment_to_db", new_callable=AsyncMock)
    @patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_routes", new_callable=AsyncMock)
    @patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_segment_traffic", new_callable=AsyncMock)
    async def test_build_routes_error_handling(
            self,
            mock_get_segment_traffic,
            mock_get_routes,
            mock_save_segment_to_db,
            mock_save_route_to_db,
    ):
        mock_get_routes.return_value = [
            {
                "summary": "Route 1",
                "legs": [
                    {
                        "distance": {"text": "10 km", "value": 10000},
                        "duration_in_traffic": {"text": "20 mins", "value": 1200},
                        "steps": [],  # Порожній список кроків
                    }
                ],
            }
        ]

        # Мокування відповіді від GoogleAPIConnector.get_segment_traffic
        mock_get_segment_traffic.return_value = {
            "duration_in_traffic": {"value": 600},
            "duration": {"value": 500},
        }

        # Ініціалізація RouteBuilder
        route_builder = RouteBuilder(GoogleAPIConnector())

        # Виклик методу build_routes
        origin = (50.4501, 30.5234)
        destination = (50.4519, 30.5223)
        db_session = AsyncMock()

        result = await route_builder.build_routes(origin, destination, db_session)

        # Перевірка, що маршрут з помилковими сегментами оброблено
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["segments"], [])  # Очікуємо, що сегментів немає

        # Перевірка, що save_route_to_db викликалась
        mock_save_route_to_db.assert_called_once_with(
            mock_get_routes.return_value[0]["legs"][0], db_session
        )

        # Перевірка, що save_segment_to_db не викликалась через пусті steps
        mock_save_segment_to_db.assert_not_called()

        # Перевірка, що get_segment_traffic не викликається для пустих steps
        mock_get_segment_traffic.assert_not_called()
