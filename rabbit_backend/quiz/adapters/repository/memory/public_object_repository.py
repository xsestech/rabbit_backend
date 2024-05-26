from typing import Protocol, TypeVar
from uuid import UUID

from rabbit_backend.quiz.entities import PublicObjectEntity

PublicObjectType = TypeVar("PublicObjectType", bound=PublicObjectEntity)


class PublicObjectRepository(Protocol[PublicObjectType]):
    def get_by_id(self, object_id: UUID) -> PublicObjectType:
        ...

    def delete(self, object_id: UUID) -> None:
        ...

    def update(self, public_object: PublicObjectType) -> PublicObjectType:
        ...
