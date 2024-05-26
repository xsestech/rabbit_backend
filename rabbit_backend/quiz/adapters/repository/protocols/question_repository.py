from typing import Protocol

from rabbit_backend.quiz.adapters.repository.protocols.public_object_repository import (
    PublicObjectRepository,
)
from rabbit_backend.quiz.entities import QuestionEntityAbstract


class QuestionRepository(PublicObjectRepository[QuestionEntityAbstract], Protocol):
    pass
