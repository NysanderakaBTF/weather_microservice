from config.db_config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import BigInteger, Text


class City(Base):
    __tablename__ = 'cities'
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    weather = relationship("Weather", back_populates="city")
