from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = 'redis'
    redis_port: int = 6379

    model_config = ConfigDict(env_file='.env', arbitrary_types_allowed=True)


settings = Settings()
