from typing import Any, Optional, Protocol
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import QuestionEntityAbstract, TopicEntity
from rabbit_backend.user.entities import UserEntity


class QuestionRepository(PublicObjectRepository[QuestionEntityAbstract], Protocol):
    def add(
        self,
        data: dict[str, Any],
        topic_id: UUID,
    ) -> QuestionEntityAbstract:
        ...

    def fill_topic(
        self,
        topic: TopicEntity,
        user: UserEntity,
        limit: Optional[int] = 200,
    ) -> TopicEntity:
        ...
