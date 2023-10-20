# Weather app

This application contains 2 services:

1. Parser for weather that utilise Celery for scheduling requests
2. Api that contains 3 endpoints:
   1. POST /weather/{city} - for creating City in db
   2. GET /weather - for retrieving list of cities with latest weather (has param "search" for searching city by name)
   3. GET /weather/{city_id} - for getting info about city weather and average weather data in given period (required params "start", "end" - timestamp without timezone)

Database - PosgreSQL, it was chosen due to it's relaibility and popularity

## Starting app

To start app you need Docker, Docker compose and internet connection. To start app write:

```shell
docker compose up
```

after initialization and startup you can access API on address: http://localhost:8080/docs
