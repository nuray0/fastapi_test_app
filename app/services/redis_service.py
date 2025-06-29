import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


async def save_request_response(key: str, data: dict):
    await redis_client.rpush(key, str(data))


async def get_all_by_key(key: str):
    return await redis_client.lrange(key, 0, -1)
