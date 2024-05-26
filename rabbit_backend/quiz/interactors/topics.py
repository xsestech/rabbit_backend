from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.topic_repository import (
    TopicRepository,
)
from rabbit_backend.quiz.entities import TopicEntity
from rabbit_backend.quiz.interactors.dtos.topic_dtos import (
    TopicCreateDTO,
    TopicDTO,
    TopicEditDTO,
)
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.public_object_base import GetPublicObjectEntity
from rabbit_backend.quiz.interactors.questions import DeleteQuestionUseCase
from rabbit_backend.user.repository.protocols.user_repository import UserRepository
from rabbit_backend.utlis import zero_uuid


class TopicDependencyMixin:
    def __init__(
        self,
        topic_repository: TopicRepository,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._topic_repository = topic_repository
        self._question_repository = question_repository
        self._user_repository = user_repository


class AddTopicUseCase(TopicDependencyMixin):
    def __call__(self, topic_dto: TopicCreateDTO) -> TopicDTO:
        user = self._user_repository.get_by_id(topic_dto.user_id)
        topic = TopicEntity(
            id=zero_uuid(),
            name=topic_dto.name,
            user=user,
            questions_type=topic_dto.question_type,
            questions=[],
        )
        return TopicDTO.model_validate(
            self._topic_repository.add(subject_id=topic_dto.subject_id, topic=topic),
        )


class GetTopicUseCase(TopicDependencyMixin):
    def __call__(
        self,
        topic_id: UUID,
        user_id: UUID,
        limit: int = 50,
    ) -> TopicDTO:
        get_topic = GetPublicObjectEntity[TopicEntity](
            self._topic_repository,
            self._user_repository,
        )
        topic = get_topic(topic_id, user_id)
        user = self._user_repository.get_by_id(user_id)
        topic = self._question_repository.fill_topic(
            topic,
            user,
            limit=limit,
        )
        return TopicDTO.model_validate(topic)


class UpdateTopicUseCase(TopicDependencyMixin):
    def __call__(self, topic_dto: TopicEditDTO) -> None:
        topic = self._topic_repository.get_by_id(topic_dto.id)
        user = self._user_repository.get_by_id(topic_dto.user_id)
        if not topic.can_user_edit(user):
            raise PublicObjectAccessDeniedError(topic)
        topic.name = topic_dto.name
        self._topic_repository.update(topic)


class DeleteTopicUseCase(TopicDependencyMixin):
    def __call__(self, topic_id: UUID, user_id: UUID) -> None:
        user = self._user_repository.get_by_id(user_id)
        topic = self._topic_repository.get_by_id(topic_id)
        if not topic.can_user_delete(user):
            raise PublicObjectAccessDeniedError(topic)
        topic = self._question_repository.fill_topic(
            topic,
            user,
            limit=None,
        )
        for question in topic.questions:
            DeleteQuestionUseCase(..., ...)(question.id, user_id)  # TODO: DEP INJ
        self._topic_repository.delete(topic_id)
