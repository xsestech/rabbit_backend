from typing import Protocol
from uuid import UUID

from rabbit_backend.user.entities import UserEntity


class UserRepository(Protocol):
    def get_by_id(self, user_id: UUID) -> UserEntity:
        ...
