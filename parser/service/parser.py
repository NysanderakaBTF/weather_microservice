import aiohttp

from config.db_config import provide_session
from config.config import config
from models.city import City
from models.weather import Weather
from sqlalchemy import select


class ParserService:

    @staticmethod
    async def get_and_write_weather():
        async with provide_session() as session:
            res = await session.execute(select(City))
            cities = res.scalars().all()
            await session.commit()

        weathers = []

        for city in cities:
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await session.get(f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={config.OPENWEATHERMAP_KEY}')
                    resp = await resp.json()
                except Exception as e:
                    raise e
                weathers.append(Weather(
                    city_id=city.id,
                    temperature=resp['main']['temp'],
                    pressure=resp['main']['pressure'],
                    wind_speed=resp['wind']['speed']
                ))
        async with provide_session() as db:
            db.add_all(weathers)
            await db.commit()
