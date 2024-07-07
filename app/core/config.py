
import os
from dotenv import load_dotenv
load_dotenv()
from cryptography.fernet import Fernet
import base64

class Settings:
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    DATABASE_URL:str = os.getenv("DATABASE_URL")
    JWT_EXPIRATION_SECONDS: int = 60000
    REDIS_URL: str = os.getenv("REDIS_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

settings = Settings()
