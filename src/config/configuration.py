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
    sender_email: str = ""
    sender_password: str = ""
    recipient_email: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

configuration: Configuration = Configuration()
