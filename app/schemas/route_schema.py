from pydantic import BaseModel

class RouteSchema(BaseModel):
    start_location: str
    end_location: str
    waypoints: list