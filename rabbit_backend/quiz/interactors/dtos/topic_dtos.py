from pydantic import UUID4, field_validator

from rabbit_backend.quiz.entities import QuestionEntityAbstract
from rabbit_backend.quiz.interactors.dtos.dto_base import (
    DTOBase,
    PublicCreateDTOBase,
    PublicDTOBase,
)
from rabbit_backend.quiz.interactors.dtos.question_dto import QuestionDTO


class TopicCreateDTO(PublicCreateDTOBase):
    name: str
    subject_id: UUID4
    user_id: UUID4
    question_type: str


class TopicDTO(TopicCreateDTO, PublicDTOBase):
    id: UUID4
    questions: list[QuestionDTO]

    @field_validator("questions", mode="before")
    @classmethod
    def validate_topics(
        cls,
        questions: list[QuestionEntityAbstract],
    ) -> list[QuestionDTO]:
        return [QuestionDTO.model_validate(question) for question in questions]


class TopicEditDTO(DTOBase):
    id: UUID4
    name: str
    subject_id: UUID4
