from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    sqlalchemy_database_url: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
