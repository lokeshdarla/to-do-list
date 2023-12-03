from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_USERNAME:str
    DATABASE_HOSTNAME:str
    DATABASE_PORT:str
    DATABASE_PASSWORD:str
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    SECRET_KEY:str
    access_token_expire_minutes:int

    class Config:
        env_file='.env'

settings = Settings()
