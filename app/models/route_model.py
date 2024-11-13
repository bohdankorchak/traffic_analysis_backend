from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    waypoints = Column(String)
    travel_time = Column(Float)
