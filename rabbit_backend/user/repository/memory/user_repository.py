from uuid import UUID, uuid4

from rabbit_backend.user.entities import UserEntity
from rabbit_backend.user.repository.protocols.user_repository import UserRepository


class UserMemoryRepository(UserRepository):
    def __init__(self) -> None:
        self._objects: dict[UUID, UserEntity] = {}

    def add(self, user: UserEntity) -> UserEntity:
        user.id = uuid4()
        self._objects[user.id] = user
        return user

    def get_by_id(self, user_id: UUID) -> UserEntity:
        return self._objects[user_id]
