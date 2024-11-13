import unittest
from app.services.traffic_data_service import TrafficDataService

class TestTrafficDataService(unittest.TestCase):
    def test_get_traffic_data(self):
        service = TrafficDataService("test_api_key")
        self.assertIsNotNone(service)
