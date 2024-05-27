from dependency_injector import containers, providers

from rabbit_backend.quiz.containers import QuizContainer
from rabbit_backend.user.containers import UserContainer


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    user_package = providers.Container(
        UserContainer,
    )

    quiz_package = providers.Container(
        QuizContainer,
        user_repository=user_package.user_repository,
    )
