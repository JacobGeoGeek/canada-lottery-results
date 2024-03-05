from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class Environnement(Enum):
    DEV = "DEV"
    PROD = "PROD"
class Configuration(BaseSettings):
    environnement: Environnement = Environnement.DEV
    root_path: str = ""
    port: int = 8080
    host: str = "0.0.0.0"
    rapidapi_proxy_secret: str = ""
    database_connection_string: str = ""

configuration: Configuration = Configuration()
