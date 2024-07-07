import aioredis
from datetime import timedelta
from app.core.config import settings


redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(settings.REDIS_URL)
    return redis

async def set_jwt_token(token: str, username: str):
    try:
        token_encrypted = settings.cipher_suite.encrypt(token.encode())
        redis = await get_redis()
        await redis.setex(f"token:{username}", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), token_encrypted)
    except aioredis.RedisError as e:
        print(f"Redis error occurred: {e}")
    finally:
        if redis:
            await redis.close()

async def get_token_for_user(username: str):
    try:
        redis = await get_redis()
        token_encrypted = await redis.get(f"token:{username}")
        if token_encrypted:
            # Decrypt the token
            token_decrypted = settings.cipher_suite.decrypt(token_encrypted).decode('utf-8')
            return token_decrypted
        return None
    except aioredis.RedisError as e:
        print(f"Redis error occurred: {e}")
        return None
    finally:
        if redis:
            await redis.close()
