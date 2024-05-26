from typing import Generic, TypeVar
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import PublicObjectEntity
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.user.repository.protocols.user_repository import UserRepository

PublicObjectEntityType = TypeVar("PublicObjectEntityType", bound=PublicObjectEntity)


class GetPublicObjectEntity(Generic[PublicObjectEntityType]):
    def __init__(
        self,
        repository: PublicObjectRepository[PublicObjectEntityType],
        user_repository: UserRepository,
    ) -> None:
        self._repository = repository
        self._user_repository = user_repository

    def __call__(self, object_id: UUID, user_id: UUID) -> PublicObjectEntityType:
        public_object = self._repository.get_by_id(object_id)
        user = self._user_repository.get_by_id(user_id)
        if public_object.can_user_read(user):
            raise PublicObjectAccessDeniedError(public_object)
        self._user = user

        return public_object
