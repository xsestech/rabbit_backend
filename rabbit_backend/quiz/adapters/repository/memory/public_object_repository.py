from typing import Callable, Generic, TypeVar
from uuid import UUID

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
        limit: int = 50,
    ) -> list[PublicObjectType]:
        return [obj for obj in self._objects.values() if filter_func(obj)][:limit]


ParentType = TypeVar(
    "ParentType",
    bound=PublicObjectEntity,
)


class ChildPublicObjectMemoryRepository(
    PublicObjectMemoryRepository[PublicObjectType],
    Generic[PublicObjectType, ParentType],
):
    def __init__(
        self,
        parent_repository: PublicObjectRepository[ParentType],
        child_attr_in_parent: str,
    ) -> None:
        super().__init__()
        self._parent_objects: dict[UUID, UUID] = {}
        self._parent_repository = parent_repository
        self._child_attr_in_parent = child_attr_in_parent

    def delete(self, topic_id: UUID) -> None:
        parent_id = self._parent_objects[topic_id]
        parent = self._parent_repository.get_by_id(parent_id)
        getattr(parent, self._child_attr_in_parent).remove(self._objects[topic_id])
        self._parent_repository.update(parent)
        super().delete(topic_id)
