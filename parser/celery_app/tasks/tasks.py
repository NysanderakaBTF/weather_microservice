import asyncio

from celery_app import celery_app
from service.parser import ParserService


@celery_app.task(name="get_and_write_weather")
def collect_weather():
    """
    The function `collect_weather` is a Celery task that collects and writes weather data using the
    `ParserService` class. 
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ParserService.get_and_write_weather())
