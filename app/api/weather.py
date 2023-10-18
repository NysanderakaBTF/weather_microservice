from fastapi import APIRouter

from app.schema.city_schema import CreateCityRequestSchema
from app.service.city_weather import CityWeatherService
from dateutil import parser

weather_router = APIRouter(prefix="/weather")


@weather_router.post('/{city}')
async def create_city(city: str):
    return await CityWeatherService.create_city(CreateCityRequestSchema(name=city))


@weather_router.get('')
async def list_city(search: str = ""):
    return await CityWeatherService.get_city_list(search)


@weather_router.get('/{city_id}')
async def avg(city_id:int, end:str, start:str):
    end_dt = parser.parse(end)
    start_dt = parser.parse(start)
    return await CityWeatherService.get_avg_and_all_data_for_period(city_id, start_dt, end_dt)