from core.db.db_config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import BigInteger, Text


# The City class represents a city in a database table, with attributes for id, name, and a
# relationship to the Weather class.
class City(Base):
    __tablename__ = 'cities'
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    weather = relationship("Weather", back_populates="city")
