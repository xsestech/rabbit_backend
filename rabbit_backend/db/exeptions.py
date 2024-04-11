import functools
from typing import Any, Callable, Dict

from fastapi import HTTPException


class BackendException(Exception):
    """TODO: Docstring"""

    def __init__(self, error_code: str, msg: str, status_code: int) -> None:
        self.__status_code = status_code
        self.__error_code = error_code
        self.__msg = msg

    @property
    def detail(self) -> Dict[str, Any]:
        if not (self.__error_code or self.__msg):
            raise NotImplementedError("Error code or message wasn't defined")
        return {
            "msg": self.__msg,
            "code": self.__error_code,
        }

    @property
    def status_code(self) -> int:
        if not self.__status_code:
            raise NotImplementedError("Status code wasn't defined")
        return self.__status_code


class TopicNameIsNotUnique(BackendException):
    def __init__(self) -> None:
        super().__init__(
            error_code="UNUNIQUE_NAME",
            msg="This topic name is already exists",
            status_code=400,
        )


class TopicIdDoesNotExists(BackendException):
    """TODO: Docstring"""

    def __init__(self) -> None:
        super().__init__(
            error_code="INVALID_TOPIC_ID",
            msg="This topic ID doesn't exist. Check the entered ID",
            status_code=404,
        )


def backend_exception(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except BackendException as exception:
            raise HTTPException(
                status_code=exception.status_code,
                detail=exception.detail,
            )

    return wrapper
