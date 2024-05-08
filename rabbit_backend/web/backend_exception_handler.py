import functools
from typing import Any, Callable

from fastapi import HTTPException

from rabbit_backend.db.exceptions import BackendError


def backend_exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle backend exceptions.

    It will raise a fastapi HTTPException with status code and detail from the exception

    Parameters
    ----------
    func : Callable[..., Any]
        Function to be decorated

    Returns
    -------
    Callable[..., Any]
        The decorated function
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except BackendError as exception:
            raise HTTPException(
                status_code=exception.status_code,
                detail=exception.detail,
            )

    return wrapper
