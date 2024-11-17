# Тест test_save_route_to_db:
# Перевіряє, чи створюється екземпляр класу Route.
# Перевіряє, чи передаються правильні значення в db_session.add.

# Тест test_save_segment_to_db:
# Перевіряє, чи створюється екземпляр класу RouteSegment.
# Аналогічно перевіряє, чи правильні значення додаються у db_session.

import unittest
from unittest.mock import AsyncMock
from backend.app.models.route_model import save_route_to_db, save_segment_to_db, Route, RouteSegment


class TestRouteModelMethods(unittest.IsolatedAsyncioTestCase):
    async def test_save_route_to_db(self):
        route_data = {
            "start_address": "Start Address",
            "start_location": {"lat": 50.4501, "lng": 30.5234},
            "end_address": "End Address",
            "end_location": {"lat": 50.4519, "lng": 30.5223},
            "distance": {"text": "10 km", "value": 10000},
            "duration": {"text": "15 mins", "value": 900},
            "duration_in_traffic": {"text": "20 mins", "value": 1200},
        }

        db_session = AsyncMock()

        await save_route_to_db(route_data, db_session)

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

        added_route = db_session.add.call_args[0][0]
        self.assertIsInstance(added_route, Route)
        self.assertEqual(added_route.start_address, "Start Address")
        self.assertEqual(added_route.start_lat, 50.4501)
        self.assertEqual(added_route.start_lng, 30.5234)
        self.assertEqual(added_route.end_address, "End Address")
        self.assertEqual(added_route.end_lat, 50.4519)
        self.assertEqual(added_route.end_lng, 30.5223)
        self.assertEqual(added_route.distance_text, "10 km")
        self.assertEqual(added_route.distance_value, 10000)
        self.assertEqual(added_route.duration_text, "15 mins")
        self.assertEqual(added_route.duration_value, 900)
        self.assertEqual(added_route.duration_in_traffic_text, "20 mins")
        self.assertEqual(added_route.duration_in_traffic_value, 1200)

    async def test_save_segment_to_db(self):
        segment_data = {
            "start_location": {"lat": 50.4501, "lng": 30.5234},
            "end_location": {"lat": 50.4519, "lng": 30.5223},
            "duration_in_traffic": 120,
            "normal_duration": 100,
            "polyline": "mock_polyline",
        }

        db_session = AsyncMock()

        await save_segment_to_db(segment_data, db_session)

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()

        added_segment = db_session.add.call_args[0][0]
        self.assertIsInstance(added_segment, RouteSegment)
        self.assertEqual(added_segment.start_lat, 50.4501)
        self.assertEqual(added_segment.start_lng, 30.5234)
        self.assertEqual(added_segment.end_lat, 50.4519)
        self.assertEqual(added_segment.end_lng, 30.5223)
        self.assertEqual(added_segment.duration_in_traffic, 120)
        self.assertEqual(added_segment.normal_duration, 100)
        self.assertEqual(added_segment.polyline, "mock_polyline")
