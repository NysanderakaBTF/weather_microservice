from config.db_config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import BigInteger, Float, TIMESTAMP
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy import func


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
