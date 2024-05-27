from typing import Any

from pydantic import UUID4, BaseModel, field_validator

from rabbit_backend.quiz.interactors.dtos.dto_base import (
    PublicCreateDTOBase,
    PublicDTOBase,
)


class QuestionCreateDTO(PublicCreateDTOBase):
    data: dict[str, Any]
    topic_id: UUID4

    @field_validator("data", mode="before")
    @classmethod
    def validate_data(cls, data: BaseModel) -> dict[str, Any]:
        return data.dict()


class QuestionDTO(QuestionCreateDTO, PublicDTOBase):
    id: UUID4
