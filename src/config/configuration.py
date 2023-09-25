from pydantic_settings import BaseSettings

class Configuration(BaseSettings):
    environnement: str = "DEV"
    root_path: str = ""
    port: int = 8080
    host: str = "0.0.0.0"

configuration: Configuration = Configuration()
