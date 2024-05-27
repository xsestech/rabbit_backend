from dependency_injector import containers, providers

from rabbit_backend.quiz.adapters.repository.memory.question_repository import (
    QuestionMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.subject_repository import (
    SubjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.topic_repository import (
    TopicMemoryRepository,
)
from rabbit_backend.user.repository.protocols.user_repository import UserRepository


class QuizContainer(containers.DeclarativeContainer):
    user_repository: UserRepository = providers.Dependency()

    subject_repository = providers.Singleton(SubjectMemoryRepository)
    topic_repository = providers.Singleton(
        TopicMemoryRepository,
        subject_repository=subject_repository,
    )
    question_repository = providers.Singleton(
        QuestionMemoryRepository,
        topic_repository=topic_repository,
    )
