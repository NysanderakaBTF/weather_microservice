from typing import List

from pydantic import BaseModel, Field

from app.schema.weather_schema import WeatherInfoSchema


class CreateCityRequestSchema(BaseModel):
    name: str = Field(..., description="Name of the city")

class CreateCityResourceSchema(BaseModel):
    id: int = Field(..., description="id of the city in db")
    name: str = Field(..., description="Name of the city")

class GetCitySchema(CreateCityResourceSchema):
    weather: List[WeatherInfoSchema]
    