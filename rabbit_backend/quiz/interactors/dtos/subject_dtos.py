from pydantic import UUID4, field_validator

from rabbit_backend.quiz.entities import TopicEntity
from rabbit_backend.quiz.interactors.dtos.dto_base import (
    PublicCreateDTOBase,
    PublicDTOBase,
)
from rabbit_backend.quiz.interactors.dtos.topic_dtos import TopicDTO


class SubjectCreateDTO(PublicCreateDTOBase):
    name: str


class SubjectDTO(PublicDTOBase):
    id: UUID4
    name: str
    topics: list[TopicDTO]

    @field_validator("topics", mode="before")
    @classmethod
    def validate_topics(cls, topics: list[TopicEntity]) -> list[TopicDTO]:
        return [TopicDTO.model_validate(topic) for topic in topics]
