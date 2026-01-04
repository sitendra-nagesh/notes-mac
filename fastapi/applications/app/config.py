# from pydantic import BaseSettings
from pydantic.v1 import BaseSettings

class Settings(BaseSettings): # Case insensitive
    # database_hostname: str = "localhost"
    # database_username: str = "postgres"
    # SECRET_KEY: str = "random_password"
    # path: str

    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file="app/.env"


settings = Settings()

# print(settings.database_hostname)