import asyncio

from celery_app import celery_app
from service.parser import ParserService


@celery_app.task(name="get_and_write_weather")
def collect_weather():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ParserService.get_and_write_weather())
