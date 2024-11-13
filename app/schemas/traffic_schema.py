from pydantic import BaseModel

class TrafficSchema(BaseModel):
    segment_id: int
    traffic_intensity: int
    average_speed: float
