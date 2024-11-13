from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.database import Base

class Traffic(Base):
    __tablename__ = "traffic"
    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, nullable=False)
    traffic_intensity = Column(Integer)
    average_speed = Column(Float)
    last_updated = Column(TIMESTAMP)
