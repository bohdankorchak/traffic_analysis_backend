import unittest
from backend.app.services.utils import decode_polyline


class TestDecodePolyline(unittest.TestCase):
    def test_decode_valid_polyline(self):
        encoded = "gfo}EtohhUxD@bAxJmGF"
        expected_points = [
            [36.45556, -116.86667],
            [36.45463, -116.86668],
            [36.45429, -116.86857],
            [36.45564, -116.86861],
        ]

        result = decode_polyline(encoded)
        self.assertEqual(result, expected_points)

    def test_decode_empty_polyline(self):
        encoded = ""
        expected_points = []

        result = decode_polyline(encoded)
        self.assertEqual(result, expected_points)

    def test_decode_invalid_polyline(self):
        encoded = "invalid_polyline"

        with self.assertRaises(IndexError):
            decode_polyline(encoded)

