""""main.py"""
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from lottomax import lottomax_route
from config.configuration import configuration, Environnement
from security.security_service import validate_rapidapi_proxy_secret


app = FastAPI(
    title="Canada lottery API",
    description="API for Canada lottery results",
    version="0.0.1",
    root_path=configuration.root_path,
    dependencies=[Depends(validate_rapidapi_proxy_secret)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lottomax_route.router)

@app.get("/", summary="API version", include_in_schema=False)
async def root():
    return {"message": "Canada lottery API", "version": "0.0.1"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=configuration.host, port=configuration.port, reload=configuration.environnement == Environnement.DEV)