from uuid import UUID

from typing_extensions import override

from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.subject_repository import (
    SubjectRepository,
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
from rabbit_backend.quiz.interactors.public_object_base import (
    GetPublicObjectEntity,
    PublishObjectUseCase,
)
from rabbit_backend.quiz.interactors.questions import DeleteQuestionUseCase
from rabbit_backend.user.repository.protocols.user_repository import UserRepository
from rabbit_backend.utlis import zero_uuid


class PublishTopicUseCase(PublishObjectUseCase[TopicEntity]):
    def __init__(
        self,
        topic_repository: TopicRepository,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ):
        self._question_repository = question_repository
        self._topic_repository = topic_repository
        super().__init__(topic_repository, user_repository)

    @override
    def __call__(
        self,
        object_id: UUID,
        user_id: UUID,
        publish: bool = True,
    ) -> None:
        super().__call__(object_id, user_id, publish)
        user = self._user_repository.get_by_id(user_id)
        topic = self._topic_repository.get_by_id(object_id)
        topic = self._question_repository.fill_topic(topic, user, limit=None)
        publish_question = PublishObjectUseCase(
            self._question_repository,
            self._user_repository,
        )
        for question in topic.questions:
            publish_question(question.id, user_id, publish)


class TopicDependencyMixin:
    def __init__(
        self,
        topic_repository: TopicRepository,
        user_repository: UserRepository,
    ) -> None:
        self._topic_repository = topic_repository
        self._user_repository = user_repository


class AddTopicUseCase(TopicDependencyMixin):
    def __init__(
        self,
        subject_repository: SubjectRepository,
        topic_repository: TopicRepository,
        user_repository: UserRepository,
    ) -> None:
        self._subject_repository = subject_repository
        super().__init__(topic_repository, user_repository)

    def __call__(self, topic_dto: TopicCreateDTO) -> TopicDTO:
        user = self._user_repository.get_by_id(topic_dto.user_id)
        subject = self._subject_repository.get_by_id(topic_dto.subject_id)
        if not subject.can_user_read(user):
            raise PublicObjectAccessDeniedError(subject)
        topic = TopicEntity(
            id=zero_uuid(),
            name=topic_dto.name,
            user=user,
            question_type=topic_dto.question_type,
            questions=[],
            subject=subject,
        )
        return TopicDTO.model_validate(
            self._topic_repository.add(topic=topic),
        )


class GetTopicUseCase(TopicDependencyMixin):
    def __init__(
        self,
        topic_repository: TopicRepository,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ):
        self._question_repository = question_repository
        super().__init__(topic_repository, user_repository)

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
    def __init__(
        self,
        subject_repository: SubjectRepository,
        topic_repository: TopicRepository,
        user_repository: UserRepository,
    ) -> None:
        self._subject_repository = subject_repository
        super().__init__(topic_repository, user_repository)

    def __call__(self, topic_dto: TopicEditDTO, user_id: UUID) -> None:
        topic = self._topic_repository.get_by_id(topic_dto.id)
        user = self._user_repository.get_by_id(user_id)
        subject = self._subject_repository.get_by_id(topic_dto.subject_id)
        if not topic.can_user_edit(user) or not subject.can_user_read(user):
            raise PublicObjectAccessDeniedError(topic)
        topic.name = topic_dto.name
        topic.subject = subject
        self._topic_repository.update(topic)


class DeleteTopicUseCase:
    def __init__(
        self,
        topic_repository: TopicRepository,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._topic_repository = topic_repository
        self._question_repository = question_repository
        self._user_repository = user_repository

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
        delete_question = DeleteQuestionUseCase(
            self._topic_repository,
            self._question_repository,
            self._user_repository,
        )
        for question in topic.questions:
            delete_question(question.id, user_id)
        self._topic_repository.delete(topic_id)
