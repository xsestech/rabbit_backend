from typing import Optional, Protocol
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import TopicEntity


class TopicRepository(PublicObjectRepository[TopicEntity], Protocol):
    def add(self, subject_id: UUID, topic: TopicEntity) -> TopicEntity:
        ...

    def fill_questions(
        self,
        topic: TopicEntity,
        limit: Optional[int] = 50,
        is_unpublished_included: bool = True,
    ) -> TopicEntity:
        ...
