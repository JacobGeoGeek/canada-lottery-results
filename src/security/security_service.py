from typing import Annotated
from fastapi import Header, HTTPException, status
from config.configuration import configuration

def validate_rapidapi_proxy_secret(x_rapid_api_proxy_secret: Annotated[str | None, Header(..., description="The RapidAPI Proxy Secret")] = None):
    """Validate the RapidAPI Proxy Secret"""
    if configuration.environnement == "PROD" and x_rapid_api_proxy_secret != configuration.rapidapi_proxy_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-RapidAPI-Proxy-Secret header")
    