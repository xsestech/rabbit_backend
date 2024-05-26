from pydantic import UUID4

from rabbit_backend.quiz.interactors.dtos.dto_base import (
    PublicCreateDTOBase,
    PublicDTOBase,
)


class TopicCreateDTO(PublicCreateDTOBase):
    name: str
    subject_id: UUID4
    user_id: UUID4
    question_type: str


class TopicDTO(TopicCreateDTO, PublicDTOBase):
    id: UUID4


class TopicEditDTO(PublicDTOBase):
    id: UUID4
    name: str
