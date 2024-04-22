from typing import Annotated
from fastapi import Header, HTTPException
from config.configuration import configuration, Environnement

def validate_rapidapi_proxy_secret(x_rapidAPI_proxy_secret: Annotated[str | None, Header(..., description="The RapidAPI Proxy Secret")] = None):
    """Validate the RapidAPI Proxy Secret"""
    if configuration.environnement == Environnement.PROD  and x_rapidAPI_proxy_secret != configuration.rapidapi_proxy_secret:
        raise HTTPException(status_code=401, detail="Invalid X-RapidAPI-Proxy-Secret header")
