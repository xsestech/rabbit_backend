from typing import Optional, Protocol
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity


class SubjectRepository(PublicObjectRepository[SubjectEntity], Protocol):
    def add(self, subject: SubjectEntity) -> SubjectEntity:
        ...

    def list(
        self,
        user_id: UUID,
        limit: int = 50,
        is_unpublished_included: bool = True,
    ) -> list[SubjectEntity]:
        ...

    def fill_topics(
        self,
        subject: SubjectEntity,
        limit: Optional[int] = 50,
        is_unpublished_included: bool = True,
    ) -> SubjectEntity:
        ...
