from fastapi import FastAPI
from redis.asyncio import ConnectionPool

from rabbit_backend.settings import settings


def init_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection pool for redis.

    Parameters
    ----------
    app : FastAPI
         current fastapi application.
    """
    app.state.redis_pool = ConnectionPool.from_url(
        str(settings.redis_url),
    )


async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Closes redis connection pool.

    Parameters
    ----------
    app : FastAPI
         current fastapi application.
    """
    await app.state.redis_pool.disconnect()
