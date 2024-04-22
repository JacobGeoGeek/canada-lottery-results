""""main.py"""
from contextlib import asynccontextmanager
from typing import Final
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from lottomax import lottomax_route
from six_fourty_nine import six_fourty_nine_route
from daily_grand import daily_grand_route
from config.configuration import configuration, Environnement
from security.security_service import validate_rapidapi_proxy_secret
from scheduler.scheduler import Scheduler

scheduler: Final[Scheduler] = Scheduler()

@asynccontextmanager
async def life_span(app: FastAPI) :
    scheduler.start()
    yield
    scheduler.stop()

app = FastAPI(
    title="Canada lottery API",
    description="API for Canada lottery results",
    version="1.0.0",
    root_path=configuration.root_path,
    dependencies=[Depends(validate_rapidapi_proxy_secret)],
    lifespan=life_span
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lottomax_route.router)
app.include_router(six_fourty_nine_route.router)
app.include_router(daily_grand_route.router)

@app.get("/", summary="API version", include_in_schema=False)
async def root():
    return {"message": app.title, "version": app.version}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=configuration.host, port=configuration.port, reload=configuration.environnement == Environnement.DEV)