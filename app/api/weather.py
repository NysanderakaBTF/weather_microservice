from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query

from app.schema.city_schema import CreateCityRequestSchema, CreateCityResponceSchema, GetCityInfoSchema, GetCitySchema
from app.service.city_weather import CityWeatherService
from dateutil import parser

from dateutil.parser import ParserError

weather_router = APIRouter(prefix="/weather")


@weather_router.post('/{city}',
                     description="Creates city record in db by given name, checks if such city exists",
                     response_model=CreateCityResponceSchema)
async def create_city(city: str):
    """
        The function creates a city weather record using the provided city name.

        :param city: The `city` parameter is a string that represents the name of the city for which we want
        to create a city weather entry
        :type city: str
        :return: the result of the `CityWeatherService.create_city` method, which is likely an object
        representing the created city weather.
    """
    return await CityWeatherService.create_city(CreateCityRequestSchema(name=city))


@weather_router.get('',
                    description="Returns a list of all cities with latest weather record",
                    response_model=List[GetCitySchema]
                    )
async def list_city(search: str = ""):
    return await CityWeatherService.get_city_list(search)


@weather_router.get('/{city_id}',
                    description="Returns weather for city in selected period and average weather values",
                    response_model=GetCityInfoSchema
                    )
async def avg(city_id: int,
              end: Annotated[str, Query(example='2023-10-20T14:04:16.910')],
              start: Annotated[str, Query(example='2023-10-20T14:04:16.910')]):
    try:
        end_dt = parser.parse(end)
    except ParserError:
        raise HTTPException(400, detail="Incorrect timestamp for end")

    try:
        start_dt = parser.parse(start)
    except ParserError:
        raise HTTPException(400, detail="Incorrect timestamp for start")

    if end_dt <= start_dt:
        raise HTTPException(
            400, detail="End timestamp must be greater than start")

    return await CityWeatherService.get_avg_and_all_data_for_period(city_id, start_dt, end_dt)
