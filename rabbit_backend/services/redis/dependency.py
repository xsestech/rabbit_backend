from typing import AsyncGenerator

from redis.asyncio import Redis
from starlette.requests import Request


async def get_redis_pool(
    request: Request,
) -> AsyncGenerator[Redis, None]:  # pragma: no cover
    """
    Returns connection pool.

    I use pools, so you don't acquire connection till the end of the handler.

    Example
    -------
    You can use it like this:

    >>> from redis.asyncio import ConnectionPool, Redis
    >>>
    >>> async def handler(redis_pool: ConnectionPool = Depends(get_redis_pool)):
    >>>     async with Redis(connection_pool=redis_pool) as redis:
    >>>         await redis.get('key')

    Parameters
    ----------
    request: Request
        current request.

    Returns
    -------
    AsyncGenerator[Redis, None]
        redis connection pool.
    """
    return request.app.state.redis_pool
