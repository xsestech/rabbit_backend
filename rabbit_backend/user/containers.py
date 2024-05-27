from dependency_injector import containers, providers

from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository


class UserContainer(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserMemoryRepository)
