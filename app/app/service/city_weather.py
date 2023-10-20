from datetime import datetime

import aiohttp
from fastapi import HTTPException
from sqlalchemy import exists, select, func, and_
from sqlalchemy.orm import joinedload, contains_eager

from app.models.city import City
from app.models.weather import Weather
from app.schema.city_schema import CreateCityRequestSchema, CreateCityResponceSchema, GetCitySchema
from core.config import config
from core.db.db_config import provide_session


class CityWeatherService:

    @staticmethod
    async def create_city(city_schema: CreateCityRequestSchema):
        """
        The function `create_city` makes an API call to OpenWeatherMap to get weather data for a given city, 
        insuring that city with such name exists, saves the city information to a database,
        and returns the created city's ID and name.

        :param city_schema: The `city_schema` parameter is an instance of the `CreateCityRequestSchema`
        class. It is used to pass the data required to create a new city.
        :type city_schema: CreateCityRequestSchema
        :return: The function `create_city` is returning an instance of the `CreateCityResourceSchema` class
        with the `id` and `name` attributes of the created city.
        """

        # check if such city already in database
        async with provide_session() as session:
            res = await session.execute(select(exists()
                                        .where(func.lower(City.name) == func.lower(city_schema.name))))
            res = res.scalar()
            print(res)
            if res:
                raise HTTPException(
                    400, detail="Such city already in database")

        async with aiohttp.ClientSession() as session:
            try:
                resp = await session.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city_schema.name}&appid={config.OPENWEATHERMAP_KEY}')
            except Exception as e:
                print(e)
                raise HTTPException(400, detail=e)
            print(resp)
            print(resp.status)
            if resp.status != 200:
                raise HTTPException(400, detail="No such city")
            response = await resp.json()
            print(response)
            async with provide_session() as db:
                city = City(**city_schema.dict())
                db.add(city)
                await db.commit()
                db.refresh(city)
                return city

    @staticmethod
    async def get_city_list(search: str = ""):
        """
        The `get_city_list` function retrieves a list of cities with their latest weather information,
        filtered by a name.

        :param search: The `search` parameter is a string that is used to filter the city list based on the
        city name. It is an optional parameter, so if no value is provided, all cities will be returned. If
        a value is provided, the city list will be filtered to only include cities whose name contains it
        :type search: str
        :return: The function `get_city_list` returns a list of `City` objects that match the search
        criteria.
        """
        async with provide_session() as session:
            # subquery to retrive id of latest weather record for a city
            subq = (
                select(Weather.id.label('latest_weather'))
                .filter(Weather.city_id == City.id)
                .order_by(Weather.timestamp.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(City)
            )
            # query that returns a list of cities and latest weather for them (uses subq)
            query = (
                select(City)
                .outerjoin(Weather, Weather.id == subq)
                .options(
                    contains_eager(City.weather)
                )
                .where(City.name.like(f"%{search}%"))
            )
            res = (await session.execute(query)).unique()
            return res.scalars().all()

    @staticmethod
    async def get_avg_and_all_data_for_period(city: int, start: datetime, end: datetime):
        """
        The function `get_avg_and_all_data_for_period` retrieves weather data for a specific city within a
        given time period and calculates the average temperature, pressure, and wind speed for that period.

        :param city: The `city` parameter is an integer representing the ID of the city for which you want
        to retrieve weather data
        :type city: int
        :param start: The `start` parameter is a `datetime` (without timezone) object representing the start
        of the period for which you want to retrieve weather data 
        :type start: datetime
        :param end: The `end` parameter is the end datetime (without timezone for the period of weather data
        you want to retrieve. It represents the latest datetime for which you want to get weather data
        :type end: datetime
        :return: The function `get_avg_and_all_data_for_period` returns a dictionary with two keys:
        'weather' and 'avg'.
        """
        async with provide_session() as session:
            query = (
                select(Weather)
                .where(and_(Weather.city_id == city,
                            Weather.timestamp >= start,
                            Weather.timestamp <= end))
            )
            query2 = (
                select(func.avg(Weather.temperature).label('avg_temp'),
                       func.avg(Weather.pressure).label('avg_pressure'),
                       func.avg(Weather.wind_speed).label('avg_wind_speed'))
                .where(and_(Weather.city_id == city,
                            Weather.timestamp >= start,
                            Weather.timestamp <= end))
                .group_by(Weather.city_id)
            )
            res = (await session.execute(query)).unique()
            a = res.scalars().all()

            if len(a) == 0:
                raise HTTPException(400, detail="No data for that period")

            res2 = (await session.execute(query2)).fetchall()
            return {'weather': a, 'avg': {
                'avg_temp': res2[0][0],
                'avg_pressure': res2[0][1],
                'avg_wind_speed': res2[0][2],
            }}
