from uuid import UUID

import pytest

from rabbit_backend.quiz.adapters.repository.memory.question_repository import (
    QuestionMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.subject_repository import (
    SubjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.topic_repository import (
    TopicMemoryRepository,
)
from rabbit_backend.user.entities import UserEntity
from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository
from rabbit_backend.utlis import zero_uuid


def create_user(
    user_repository: UserMemoryRepository,
    is_admin: bool,
) -> UUID:
    user = UserEntity(id=zero_uuid(), is_admin=is_admin)
    return user_repository.add(user).id


@pytest.fixture(scope="package")
def user_repository() -> UserMemoryRepository:
    return UserMemoryRepository()


@pytest.fixture(scope="package")
def admin_user_id(user_repository: UserMemoryRepository) -> UUID:
    return create_user(user_repository, True)


@pytest.fixture(scope="package")
def regular_user_id(user_repository: UserMemoryRepository) -> UUID:
    return create_user(user_repository, False)


@pytest.fixture
def subject_repository() -> SubjectMemoryRepository:
    return SubjectMemoryRepository()


@pytest.fixture
def topic_repository() -> TopicMemoryRepository:
    return TopicMemoryRepository()


@pytest.fixture
def question_repository() -> QuestionMemoryRepository:
    return QuestionMemoryRepository()
