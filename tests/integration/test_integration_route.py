import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_routes_endpoint(test_db):
    """Test the /routes endpoint and validate database storage."""
    mock_route_data = [
            {
                "summary": "Mocked Route",
                "legs": [
                    {
                        "distance": {"text": "10 km", "value": 10000},
                        "duration_in_traffic": {"text": "15 mins", "value": 900},
                        "duration": {"text": "10 mins", "value": 600},
                        "start_location": {"lat": 50.4501, "lng": 30.5234},
                        "end_location": {"lat": 50.4547, "lng": 30.5238},
                        "start_address": "Mock Start Address",
                        "end_address": "Mock End Address",
                        "steps": [
                            {
                                "start_location": {"lat": 50.4501, "lng": 30.5234},
                                "end_location": {"lat": 50.4547, "lng": 30.5238},
                                "polyline": {"points": "q~|rHywhyDBGDIBI?E?E?E?AACACCGIQ_@a@s@{@IMW_@EEGEA?C?A?EBE@MJIHC@A?CACACCACCGCI"},
                            }
                        ],
                    }
                ],
            }
        ]


    mock_segment_data = {
        "duration_in_traffic": {"value": 900},
        "duration": {"value": 600},
    }

    client = TestClient(app)

    with patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_routes", return_value=mock_route_data), \
            patch("backend.app.services.traffic_data_service.GoogleAPIConnector.get_segment_traffic",
                  return_value=mock_segment_data):
        response = client.post(
            "/routes",
            json={"origin": [50.4501, 30.5234], "destination": [50.4547, 30.5238]},
        )

        assert response.status_code == 200
        assert "routes" in response.json()
