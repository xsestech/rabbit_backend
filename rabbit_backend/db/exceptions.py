import re
from typing import Any, Dict

BACKEND_ERROR_MESSAGE_LEN: int = 100
CONSTANT_CASE_REGEX: re.Pattern = re.compile(r"^[A-Z_]+$")
BACKEND_ERROR_CODE_LEN: int = 50


class BackendError(Exception):
    """This is the base exception class for all the backend exceptions.

    The handler of the backend exceptions will use attribute `status_code` and `detail`
    to format the response for fastapi HTTPException.

    Parameters
    ----------
    error_code : str
        Machine readable error code. Should be formatted in CONSTANT_CASE
    status_code : int
        HTTP status code. Usually 400
    msg : str
        Human readable error message. Should be less than 100 characters

    Attributes
    ----------
    status_code
    detail


    """

    def __init__(self, error_code: str, msg: str, status_code: int) -> None:
        if not (error_code or msg or status_code):
            raise NotImplementedError("Error, status code or message wasn't defined")
        if not re.fullmatch(CONSTANT_CASE_REGEX, error_code):
            raise ValueError("Error code should be in CONSTANT_CASE")
        if (
            len(msg) > BACKEND_ERROR_MESSAGE_LEN
            or len(error_code) > BACKEND_ERROR_CODE_LEN
        ):
            raise ValueError("Error code or message is too long")
        self._status_code = status_code
        self._error_code = error_code
        self.__msg = msg

    @property
    def detail(self) -> Dict[str, Any]:  # noqa: DAR201
        """A dictionary of error detail.

        Example of `detail`:
        `{'msg': "message text", 'code': "ERROR_CODE"}`.

        """
        return {
            "msg": self.__msg,
            "code": self._error_code,
        }

    @property
    def status_code(self) -> int:
        """int: HTTP status code."""
        return self._status_code


class TopicNameIsNotUniqueError(BackendError):
    """This exception is raised when the user tries to create a topic with a name that
    already exists.

    Child of `BackendError`

    Attributes
    ----------
    status_code
    detail
    """

    def __init__(self) -> None:
        super().__init__(
            error_code="UNIQUE_NAME",
            msg="This topic name is already exists",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )


class TopicIdDoesNotExistsError(BackendError):
    """This exception is raised when the user tries to delete a topic that doesn't exist

    Child of `BackendError`

    Attributes
    ----------
    status_code
    detail
    """

    def __init__(self) -> None:
        super().__init__(
            error_code="INVALID_TOPIC_ID",
            msg="This topic ID doesn't exist. Check the entered ID",
            status_code=404,
        )
