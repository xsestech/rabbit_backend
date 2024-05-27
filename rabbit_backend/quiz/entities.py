from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import UUID4, BaseModel, Field, field_validator
from typing_extensions import override

from rabbit_backend.user.entities import UserEntity


class PublicObjectEntity(BaseModel):
    """Base class for all objects that can be published."""

    id: UUID4
    created_at: datetime = Field(default_factory=datetime.utcnow)
    edited_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = False
    user: UserEntity

    @property
    def user_id(self) -> UUID4:
        return self.user.id

    def is_user_owner(self, user: UserEntity) -> bool:
        return self.user.id == user.id

    def can_user_edit(self, user: UserEntity) -> bool:
        return self.is_user_owner(user) or user.is_admin

    def can_user_read(self, user: UserEntity) -> bool:
        return self.is_user_owner(user) or user.is_admin or self.is_published

    def can_user_delete(self, user: UserEntity) -> bool:
        return (self.is_user_owner(user) and not self.is_published) or user.is_admin


class QuestionEntityAbstract(PublicObjectEntity, ABC):
    """Abstract base class for all questions.

    You need to define a `type` field in order to use this class. You can directly
    initialize an instance of this class, one of the children classes will be created
    based on the type field.
    """

    id: UUID4
    data: BaseModel
    topic: TopicEntity

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """str: The type of question."""
        raise NotImplementedError

    @property
    def topic_id(self) -> UUID4:
        return self.topic.id


class QuestionEntityFactory:
    """Factory, that creates question objects based on the type field in data."""

    @classmethod
    def get_question(
        cls,
        data: dict[str, Any],
        **question_attrs: Any,
    ) -> QuestionEntityAbstract:
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
        question_subclasses = QuestionEntityAbstract.__subclasses__()
        for subclass in question_subclasses:
            if subclass.type() == data["type"]:
                return subclass(data=data, **question_attrs)  # type: ignore
        raise ValueError("Invalid type")


class TestQuestionEntity(QuestionEntityAbstract):
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


class CardQuestionEntity(QuestionEntityAbstract):
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


class TopicEntity(PublicObjectEntity):
    """Class representing a topic."""

    id: UUID4
    name: str
    subject: SubjectEntity
    questions: list[QuestionEntityAbstract]
    question_type: str

    @field_validator("question_type")
    @classmethod
    def validate_questions_type(cls, value: str) -> str:
        question_subclasses = QuestionEntityAbstract.__subclasses__()
        for subclass in question_subclasses:
            if subclass.type() == value:
                return value
        raise ValueError("Invalid question type")

    @property
    def subject_id(self) -> UUID4:
        """UUID4: The id of the subject."""
        return self.subject.id  # noqa: DAR201


class SubjectEntity(PublicObjectEntity):
    """Class representing a subject."""

    id: UUID4
    name: str
    topics: list[TopicEntity]

    @override
    def can_user_edit(self, user: UserEntity) -> bool:
        return user.is_admin

    @override
    def can_user_delete(self, user: UserEntity) -> bool:
        return user.is_admin
