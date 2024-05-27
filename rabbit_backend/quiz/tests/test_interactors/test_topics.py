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
from rabbit_backend.quiz.interactors.dtos.topic_dtos import TopicEditDTO
from rabbit_backend.quiz.interactors.exceptions import PublicObjectAccessDeniedError
from rabbit_backend.quiz.interactors.subjects import (
    AddSubjectUseCase,
    DeleteSubjectUseCase,
    GetSubjectUseCase,
)
from rabbit_backend.quiz.interactors.topics import GetTopicUseCase, UpdateTopicUseCase
from rabbit_backend.quiz.tests.test_interactors.dummies import create_dummy_topics
from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository

# TODO: Test type mismatch


def test_add_topic(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )

    subject, topic, topic2 = create_dummy_topics(
        subject_repository,
        topic_repository,
        user_repository,
        regular_user_id,
        admin_user_id,
    )
    subject = get_subject(subject.id, admin_user_id)
    assert len(subject.topics) == 2
    subject = get_subject(subject.id, regular_user_id)
    assert len(subject.topics) == 1


def test_get_topic(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    question_repository: QuestionMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    subject, topic, topic2 = create_dummy_topics(
        subject_repository,
        topic_repository,
        user_repository,
        regular_user_id,
        admin_user_id,
    )
    topic_1 = get_topic(topic.id, admin_user_id)
    assert topic_1.name == "test_topic"
    topic_2 = get_topic(topic2.id, regular_user_id)
    assert topic_2.name == "test_topic_2"
    with pytest.raises(PublicObjectAccessDeniedError):
        get_topic(topic.id, regular_user_id)


def test_update_topic(
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
    update_topic = UpdateTopicUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    subject, topic, topic2 = create_dummy_topics(
        subject_repository,
        topic_repository,
        user_repository,
        regular_user_id,
        admin_user_id,
    )

    subject2 = add_subject("test_subject_2", admin_user_id)
    edit_dto = TopicEditDTO(
        id=topic.id,
        name="test_topic_2",
        subject_id=subject2.id,
    )
    with pytest.raises(PublicObjectAccessDeniedError):
        update_topic(edit_dto, regular_user_id)
    update_topic(edit_dto, admin_user_id)
    topic = get_topic(topic.id, admin_user_id)
    assert topic.name == "test_topic_2"
    assert topic.subject_id == subject2.id
    subject = get_subject(subject.id, admin_user_id)
    assert len(subject.topics) == 1
    subject2 = get_subject(subject2.id, admin_user_id)
    assert len(subject2.topics) == 1
    edit_dto = TopicEditDTO(
        id=topic2.id,
        name="test_topic_2",
        subject_id=subject2.id,
    )
    with pytest.raises(PublicObjectAccessDeniedError):
        update_topic(edit_dto, user_id=regular_user_id)
    edit_dto = TopicEditDTO(
        id=topic2.id,
        name="test_topic_2",
        subject_id=subject.id,
    )
    update_topic(edit_dto, user_id=regular_user_id)


def test_delete_subject_with_topics(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    question_repository: QuestionMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> None:
    subject, topic, topic2 = create_dummy_topics(
        subject_repository,
        topic_repository,
        user_repository,
        regular_user_id,
        admin_user_id,
    )
    delete_subject = DeleteSubjectUseCase(
        subject_repository,
        topic_repository,
        question_repository,
        user_repository,
    )
    get_subject = GetSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    with pytest.raises(PublicObjectAccessDeniedError):
        delete_subject(subject.id, regular_user_id)
    delete_subject(subject.id, admin_user_id)
    with pytest.raises(ObjectDoesNotExistError):
        get_subject(subject.id, admin_user_id)
    with pytest.raises(ObjectDoesNotExistError):
        get_topic(topic.id, admin_user_id)
