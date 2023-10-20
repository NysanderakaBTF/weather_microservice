from core.db.db_config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import BigInteger, Float, TIMESTAMP
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy import func


# The Weather class represents weather data for a specific city, including temperature, pressure, wind
# speed, and timestamp.
class Weather(Base):
    __tablename__ = 'weather'
    id = Column(BigInteger, primary_key=True)
    city_id = Column(BigInteger, ForeignKey('cities.id'))
    temperature = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=False),
                       default=func.now(), onupdate=func.now(), nullable=False)

    city = relationship("City", back_populates="weather")
