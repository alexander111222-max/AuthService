import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MODE: Literal["TEST", "LOCAL", "PROD"]

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    REFRESH_TOKEN_TTL_DAYS: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env-local"))



settings = Settings()

