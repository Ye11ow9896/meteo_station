import asyncio

import uvicorn
from fastapi import FastAPI

from database import ping_postgres_database
from src.user.router import user_router
from src.auth.router import auth_router
from src.meteo_station.router import station_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(station_router)


if __name__ == "__main__":
    asyncio.run(ping_postgres_database())
    uvicorn.run("main:app", host="127.0.0.1", port=1488, reload=True)
