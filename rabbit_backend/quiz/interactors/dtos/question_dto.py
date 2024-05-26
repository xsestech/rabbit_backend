from typing import Any

from pydantic import UUID4

from rabbit_backend.quiz.interactors.dtos.dto_base import (
    PublicCreateDTOBase,
    PublicDTOBase,
)


class QuestionCreateDTO(PublicCreateDTOBase):
    data: dict[str, Any]
    topic_id: UUID4


class QuestionDTO(QuestionCreateDTO, PublicDTOBase):
    id: UUID4
