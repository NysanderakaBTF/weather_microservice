from typing import List

from pydantic import BaseModel, Field

from app.schema.weather_schema import WeatherInfoSchema


class CreateCityRequestSchema(BaseModel):
    name: str = Field(..., description="Name of the city")


class CreateCityResponceSchema(BaseModel):
    id: int = Field(..., description="id of the city in db")
    name: str = Field(..., description="Name of the city")

    class Config:
        orm_mode = True


class GetCitySchema(CreateCityResponceSchema):
    weather: List[WeatherInfoSchema] = Field(...,
                                             description="Weather records")

    class Config:
        orm_mode = True


class AverageWeatherDataSchema(BaseModel):
    avg_temp: float = Field(..., description="Average temperature")
    avg_pressure: float = Field(..., description="Average pressure")
    avg_wind_speed: float = Field(..., description="Average wind speed")


class GetCityInfoSchema(BaseModel):
    weather: List[WeatherInfoSchema] = Field(...,
                                             description="Weather records")
    avg: AverageWeatherDataSchema = Field(...,
                                          description="Average weather data")
