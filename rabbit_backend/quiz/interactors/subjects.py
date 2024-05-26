from uuid import UUID

from rabbit_backend.quiz.adapters.repository.protocols.subject_repository import (
    SubjectRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.topic_repository import (
    TopicRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity
from rabbit_backend.quiz.interactors.dtos.subject_dtos import SubjectDTO
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.public_object_base import GetPublicObjectEntity
from rabbit_backend.quiz.interactors.topics import DeleteTopicUseCase
from rabbit_backend.user.repository.protocols.user_repository import UserRepository
from rabbit_backend.utlis import zero_uuid


class SubjectDependencyMixin:
    def __init__(
        self,
        subject_repository: SubjectRepository,
        topic_repository: TopicRepository,
        user_repository: UserRepository,
    ) -> None:  # TODO: ADD DEP INJECTION
        self._subject_repository = subject_repository
        self._topic_repository = topic_repository
        self._user_repository = user_repository


class AddSubjectUseCase(SubjectDependencyMixin):
    def __call__(self, name: str, user_id: UUID) -> SubjectDTO:
        user = self._user_repository.get_by_id(user_id)
        subject = SubjectEntity(id=zero_uuid(), name=name, user=user, topics=[])
        if user.is_admin:
            raise PublicObjectAccessDeniedError(subject)
        subject = self._subject_repository.add(subject)
        return SubjectDTO.model_validate(subject)


class ListSubjectsUseCase(SubjectDependencyMixin):
    def __call__(self, user_id: UUID, limit: int = 50) -> list[SubjectDTO]:
        user = self._user_repository.get_by_id(user_id)
        return list(
            map(
                SubjectDTO.model_validate,
                self._subject_repository.list(user=user, limit=limit),
            ),
        )


class GetSubjectUseCase(SubjectDependencyMixin):
    def __call__(
        self,
        subject_id: UUID,
        user_id: UUID,
        limit: int = 50,
    ) -> SubjectDTO:
        get_subject = GetPublicObjectEntity[SubjectEntity](
            self._subject_repository,
            self._user_repository,
        )
        subject = get_subject(subject_id, user_id)
        user = self._user_repository.get_by_id(user_id)
        subject = self._topic_repository.fill_subject(subject, user, limit=limit)
        return SubjectDTO.model_validate(subject)


class DeleteSubjectUseCase:
    def __init__(
        self,
        subject_repository: SubjectRepository,
        user_repository: UserRepository,
        topic_repository: TopicRepository,
    ) -> None:  # TODO: ADD DEP INJECTION
        self._subject_repository = subject_repository
        self._user_repository = user_repository
        self._topic_repository = topic_repository

    def __call__(self, subject_id: UUID, user_id: UUID) -> None:
        subject = self._subject_repository.get_by_id(subject_id)
        user = self._user_repository.get_by_id(user_id)
        if not subject.can_user_delete(user):
            raise PublicObjectAccessDeniedError(subject)
        subject = self._topic_repository.fill_subject(
            subject=subject,
            user=user,
            limit=None,
        )
        for topic in subject.topics:
            delete_topic = DeleteTopicUseCase(
                topic_repository=self._topic_repository,
                question_repository=...,  # TODO: ADD DEP INJECTION
                user_repository=self._user_repository,
            )
            delete_topic(topic.id, user_id)
        self._subject_repository.delete(subject.id)


class UpdateSubjectNameUseCase(SubjectDependencyMixin):
    def __call__(self, subject_id: UUID, name: str, user_id: UUID) -> SubjectDTO:
        subject = self._subject_repository.get_by_id(subject_id)
        user = self._user_repository.get_by_id(user_id)
        if not user.is_admin:
            raise PublicObjectAccessDeniedError(subject)
        subject.name = name
        return SubjectDTO.model_validate(self._subject_repository.update(subject))
