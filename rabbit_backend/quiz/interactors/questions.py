from typing import Any
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.interactors.dtos.question_dto import QuestionDTO
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.public_object_base import GetPublicObjectEntity
from rabbit_backend.user.repository.protocols.user_repository import UserRepository


class QuestionDependencyMixin:
    def __init__(
        self,
        question_repository: QuestionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._question_repository = question_repository
        self._user_repository = user_repository


class AddQuestionUseCase(QuestionDependencyMixin):
    def __call__(
        self,
        data: dict[str, Any],
        question_id: UUID,
        user_id: UUID,
    ) -> QuestionDTO:
        get_question = GetPublicObjectEntity(
            self._question_repository,
            self._user_repository,
        )
        question = get_question(question_id, user_id)
        return QuestionDTO.model_validate(question)


class GetQuestionUseCase(QuestionDependencyMixin):
    def __call__(self, question_id: UUID, user_id: UUID) -> QuestionDTO:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_read(user):
            raise PublicObjectAccessDeniedError(question)
        return QuestionDTO.model_validate(question)


class EditQuestionDataUseCase(QuestionDependencyMixin):
    def __call__(
        self,
        question_id: UUID,
        user_id: UUID,
        data: dict[str, Any],
    ) -> QuestionDTO:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_edit(user):
            raise PublicObjectAccessDeniedError(question)
        self._question_repository.update(question)
        return QuestionDTO.model_validate(question)


class DeleteQuestionUseCase(QuestionDependencyMixin):
    def __call__(self, question_id: UUID, user_id: UUID) -> None:
        user = self._user_repository.get_by_id(user_id)
        question = self._question_repository.get_by_id(question_id)
        if not question.can_user_delete(user):
            raise PublicObjectAccessDeniedError(question)
        self._question_repository.delete(question_id)
