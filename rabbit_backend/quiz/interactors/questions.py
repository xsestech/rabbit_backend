from typing import Any
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.exceptions import QuestionTypeMismatchError
from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.topic_repository import (
    TopicRepository,
)
from rabbit_backend.quiz.entities import QuestionEntityAbstract, QuestionEntityFactory
from rabbit_backend.quiz.interactors.dtos.question_dto import QuestionDTO
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.public_object_base import PublishObjectUseCase
from rabbit_backend.user.repository.protocols.user_repository import UserRepository
from rabbit_backend.utlis import zero_uuid

PublishQuestionUseCase = PublishObjectUseCase[QuestionEntityAbstract]


class QuestionDependencyMixin:
    def __init__(
        self,
        topic_repository: TopicRepository,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._question_repository = question_repository
        self._user_repository = user_repository
        self._topic_repository = topic_repository


class AddQuestionUseCase(QuestionDependencyMixin):
    def __call__(
        self,
        data: dict[str, Any],
        topic_id: UUID,
        user_id: UUID,
    ) -> QuestionDTO:
        user = self._user_repository.get_by_id(user_id)
        topic = self._topic_repository.get_by_id(topic_id)
        if not topic.can_user_edit(user):
            raise PublicObjectAccessDeniedError(topic)

        question = QuestionEntityFactory.get_question(
            id=zero_uuid(),
            data=data,
            topic=topic,
            user=user,
            is_published=topic.is_published,
        )
        if question.type() != topic.question_type:
            raise QuestionTypeMismatchError(question, topic)
        self._question_repository.add(question)
        return QuestionDTO.model_validate(question)


class GetQuestionUseCase(QuestionDependencyMixin):
    def __call__(self, question_id: UUID, user_id: UUID) -> QuestionDTO:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_read(user):
            raise PublicObjectAccessDeniedError(question)
        return QuestionDTO.model_validate(question)


class UpdateQuestionDataUseCase(QuestionDependencyMixin):
    def __call__(
        self,
        data: dict[str, Any],
        question_id: UUID,
        user_id: UUID,
    ) -> QuestionDTO:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_edit(user):
            raise PublicObjectAccessDeniedError(question)
        updated_question = QuestionEntityFactory.get_question(
            id=question.id,
            data=data,
            user=user,
            topic=question.topic,
            is_published=question.is_published,
            created_at=question.created_at,
            edited_at=question.edited_at,
        )
        if updated_question.type() != question.topic.question_type:
            raise QuestionTypeMismatchError(question, question.topic)
        updated_question = self._question_repository.update(updated_question)
        return QuestionDTO.model_validate(updated_question)


class DeleteQuestionUseCase(QuestionDependencyMixin):
    def __call__(self, question_id: UUID, user_id: UUID) -> None:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_delete(user):
            raise PublicObjectAccessDeniedError(question)
        self._question_repository.delete(question_id)
