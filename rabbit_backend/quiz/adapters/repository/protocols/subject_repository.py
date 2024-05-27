from typing import Protocol

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity
from rabbit_backend.user.entities import UserEntity


class SubjectRepository(PublicObjectRepository[SubjectEntity], Protocol):
    def add(self, subject: SubjectEntity) -> SubjectEntity:
        ...

    def list(
        self,
        user: UserEntity,
        limit: int = 50,
    ) -> list[SubjectEntity]:
        ...
