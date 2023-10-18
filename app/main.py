from fastapi import FastAPI

from api.weather import weather_router

app = FastAPI(
    title="Weather API",
    description="Weather API",
    version="0.0.1",
)

app.include_router(weather_router)
