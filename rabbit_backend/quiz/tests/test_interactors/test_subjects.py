from uuid import UUID

import pytest

from rabbit_backend.quiz.adapters.repository.exceptions import ObjectDoesNotExistError
from rabbit_backend.quiz.adapters.repository.memory.question_repository import (
    QuestionMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.subject_repository import (
    SubjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.topic_repository import (
    TopicMemoryRepository,
)
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.subjects import (
    AddSubjectUseCase,
    DeleteSubjectUseCase,
    GetSubjectUseCase,
    ListSubjectsUseCase,
    PublishSubjectUseCase,
    UpdateSubjectNameUseCase,
)
from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository


def test_add_subject(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    subject = add_subject(name="test", user_id=admin_user_id)
    assert subject.name == "test"
    assert subject.user_id == admin_user_id
    subject_from_db = subject_repository.get_by_id(subject.id)
    assert subject_from_db.name == "test"
    with pytest.raises(PublicObjectAccessDeniedError):
        add_subject(name="test2", user_id=regular_user_id)


def test_get_subject(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    subject = add_subject(name="test", user_id=admin_user_id)
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    subject = get_subject(subject.id, admin_user_id)
    assert subject.name == "test"
    assert subject.user_id == admin_user_id

    with pytest.raises(PublicObjectAccessDeniedError):
        get_subject(subject.id, regular_user_id)
    with pytest.raises(PublicObjectAccessDeniedError):
        subject2 = add_subject(name="test2", user_id=regular_user_id)


def test_publish_subject(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    publish_subject = PublishSubjectUseCase(
        subject_repository,
        user_repository,
    )
    subject = add_subject(name="test", user_id=admin_user_id)
    with pytest.raises(PublicObjectAccessDeniedError):
        get_subject(subject.id, regular_user_id)
    with pytest.raises(PublicObjectAccessDeniedError):
        publish_subject(subject.id, regular_user_id)
    publish_subject(subject.id, admin_user_id)
    subject = get_subject(subject.id, admin_user_id)
    assert subject.name == "test"
    assert subject.is_published


def test_update_subject(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    update_subject = UpdateSubjectNameUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    subject = add_subject(name="test", user_id=admin_user_id)
    update_subject(subject.id, "test2", admin_user_id)
    subject = get_subject(subject.id, admin_user_id)
    assert subject.name == "test2"
    with pytest.raises(PublicObjectAccessDeniedError):
        update_subject(subject.id, "test3", regular_user_id)
    subject = get_subject(subject.id, admin_user_id)
    assert subject.name == "test2"


def test_list_subjects(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    list_subjects = ListSubjectsUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    publish_subject = PublishSubjectUseCase(
        subject_repository,
        user_repository,
    )
    subjects = [
        add_subject(name="test", user_id=admin_user_id),
        add_subject(name="test2", user_id=admin_user_id),
        add_subject(name="test3", user_id=admin_user_id),
    ]
    assert subjects == list_subjects(admin_user_id)
    assert [] == list_subjects(regular_user_id)
    publish_subject(subjects[0].id, admin_user_id)
    subjects[0].is_published = True
    assert subjects[:1] == list_subjects(regular_user_id)


def test_delete_subject(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    question_repository: QuestionMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    delete_subject = DeleteSubjectUseCase(
        subject_repository,
        topic_repository,
        question_repository,
        user_repository,
    )
    subject = add_subject(name="test", user_id=admin_user_id)
    with pytest.raises(PublicObjectAccessDeniedError):
        delete_subject(subject.id, regular_user_id)
    delete_subject(subject.id, admin_user_id)
    with pytest.raises(ObjectDoesNotExistError):
        get_subject(subject.id, admin_user_id)
