from typing import Optional, Protocol

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity, TopicEntity
from rabbit_backend.user.entities import UserEntity


class TopicRepository(PublicObjectRepository[TopicEntity], Protocol):
    def add(self, topic: TopicEntity) -> TopicEntity:
        ...

    def fill_subject(
        self,
        subject: SubjectEntity,
        user: UserEntity,
        limit: Optional[int] = 50,
    ) -> SubjectEntity:
        ...
