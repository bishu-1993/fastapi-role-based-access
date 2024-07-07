
import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    DATABASE_URL:str = os.getenv("DATABASE_URL")
    JWT_EXPIRATION_SECONDS: int = 60000
    REDIS_URL: str = os.getenv("REDIS_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

settings = Settings()
