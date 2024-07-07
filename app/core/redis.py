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
        redis = await get_redis()
        await redis.setex(f"token:{token}", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), username)
    except aioredis.RedisError as e:
        print(f"Redis error occurred: {e}")
    finally:
        if redis:
            await redis.close()

async def get_user_id_from_token(token: str):
    redis = await get_redis()
    user_id = await redis.get(f"token:{token}")
    return int(user_id) if user_id else None

