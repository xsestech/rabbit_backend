import uuid

from rabbit_backend.quiz.adapters.repository.memory.public_object_repository import (
    PublicObjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.subject_repository import (
    SubjectRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity
from rabbit_backend.user.entities import UserEntity


class SubjectMemoryRepository(
    PublicObjectMemoryRepository[SubjectEntity],
    SubjectRepository,
):
    def add(self, subject: SubjectEntity) -> SubjectEntity:
        subject.id = uuid.uuid4()
        self._objects[subject.id] = subject
        return subject

    def list(self, user: UserEntity, limit: int = 50) -> list[SubjectEntity]:
        return self._filter(
            lambda sub: sub.can_user_read(user),
            limit=limit,
        )
