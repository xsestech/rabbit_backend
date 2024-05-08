from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import UUID4, BaseModel
from typing_extensions import override

from rabbit_backend.user.entities import User


class PublicObject(BaseModel):
    """Base class for all objects that can be published."""

    created_at: datetime
    edited_at: datetime
    is_published: bool
    user: User


class Question(PublicObject, ABC):
    """Abstract base class for all questions.

    You need to define a `type` field in order to use this class. You can directly
    initialize an instance of this class, one of the children classes will be created
    based on the type field.
    """

    id: UUID4
    data: BaseModel

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """str: The type of question."""
        raise NotImplementedError


class QuestionFactory:
    """Factory, that creates question objects based on the type field in data."""

    @classmethod
    def get_question(cls, data: dict[str, Any], **question_attrs: Any) -> Question:
        """Create a new instance of this class based on the type field.

        Parameters
        ----------
        data : dict
            Payload of the question.
        question_attrs : dict
            Question attributes.

        Raises
        ------
        ValueError
            If the type is not valid.
        ValueError
            If not all fields for Question class are present in kwargs.

        Returns
        -------
        Child of question.
        """
        question_subclasses = Question.__subclasses__()
        for subclass in question_subclasses:
            if subclass.type() == data["type"]:
                return subclass(data=data, **question_attrs)  # type: ignore
        raise ValueError("Invalid type")


class TestQuestion(Question):
    """Class representing a test question."""

    __test__ = False

    class DataSchema(BaseModel):
        type: str
        question: str
        answers: list[str]
        answer_idx: int

    data: DataSchema

    @override
    @classmethod
    def type(cls) -> str:  # noqa: N805
        """str: The type of question."""
        # noqa: DAR201
        return "test"  # noqa: DAR201


class CardQuestion(Question):
    """Class representing a card question."""

    class DataSchema(BaseModel):
        type: str
        question: str
        answer: str

    data: DataSchema

    @override
    @classmethod
    def type(cls) -> str:  # noqa: N805
        """str: The type of question."""
        # noqa: DAR201
        return "card"  # noqa: DAR201


class Topic(PublicObject):
    """Class representing a topic."""

    id: UUID4
    name: str
    questions: list[Question]


class Subject(PublicObject):
    """Class representing a subject."""

    id: UUID4
    name: str
    topics: list[Topic]
