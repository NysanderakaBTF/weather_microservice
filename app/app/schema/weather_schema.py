from datetime import datetime

from pydantic import BaseModel, Field


class WeatherInfoSchema(BaseModel):
    id: int = Field(..., description="Id of weather record")
    temperature: float = Field(..., description="Temperature")
    pressure: float = Field(..., description="Pressure")
    wind_speed: float = Field(..., description="Wind speed")
    timestamp: datetime = Field(..., description="Timestamp of weather record")