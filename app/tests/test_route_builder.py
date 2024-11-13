import unittest
from app.services.route_builder import RouteBuilder

class TestRouteBuilder(unittest.TestCase):
    def test_build_route(self):
        builder = RouteBuilder(None)
        self.assertIsNotNone(builder)
