from datetime import datetime

import aiohttp
from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, contains_eager

from app.models.city import City
from app.models.weather import Weather
from app.schema.city_schema import CreateCityRequestSchema, CreateCityResourceSchema
from core.config import config
from core.db.db_config import provide_session


class CityWeatherService:

    @staticmethod
    async def create_city(city_schema: CreateCityRequestSchema):
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
                return CreateCityResourceSchema(id=city.id, name=city.name)

    @staticmethod
    async def get_city_list(search: str = ""):
        async with provide_session() as session:

            subq = (
                select(Weather.id.label('latest_weather'))
                .filter(Weather.city_id == City.id)
                .order_by(Weather.timestamp.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(City)
            )

            query = (
                select(City)
                .outerjoin(Weather, Weather.id == subq)
                .options(
                    contains_eager(City.weather)
                )
                .where(City.name.like(f"%{search}%"))
            )
            res = (await session.execute(query)).unique()
            result_set = res.scalars().all()
            a = result_set
            return a

    @staticmethod
    async def get_avg_and_all_data_for_period(city: int, start: datetime, end: datetime):
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
            res2 = (await session.execute(query2)).fetchall()
            return {'weather': a, 'avg': {
                'avg_temp': res2[0][0],
                'avg_pressure': res2[0][1],
                'avg_wind_speed': res2[0][2],
            }}
