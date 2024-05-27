from typing import Callable, Optional, TypeVar
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.exceptions import ObjectDoesNotExistError
from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import PublicObjectEntity
from rabbit_backend.user.entities import UserEntity

PublicObjectType = TypeVar("PublicObjectType", bound=PublicObjectEntity)


class PublicObjectMemoryRepository(PublicObjectRepository[PublicObjectType]):
    def __init__(self) -> None:
        self._objects: dict[UUID, PublicObjectType] = {}

    def get_by_id(self, object_id: UUID) -> PublicObjectType:
        obj = self._objects.get(object_id)
        if not obj:
            raise ObjectDoesNotExistError(object_id)
        return self._objects[object_id]

    def delete(self, object_id: UUID) -> None:
        self._objects.pop(object_id)

    def update(self, public_object: PublicObjectType) -> PublicObjectType:
        self._objects[public_object.id] = public_object
        return public_object

    def _filter_with_publish(
        self,
        user: UserEntity,
        limit: int = 50,
    ) -> list[PublicObjectType]:
        return self._filter(
            lambda obj: obj.can_user_read(user),
            limit=limit,
        )

    def _filter(
        self,
        filter_func: Callable[[PublicObjectType], bool],
        limit: Optional[int] = 50,
    ) -> list[PublicObjectType]:
        if limit is None:
            limit = len(self._objects.values())
        return [obj for obj in self._objects.values() if filter_func(obj)][:limit]


ParentType = TypeVar(
    "ParentType",
    bound=PublicObjectEntity,
)
