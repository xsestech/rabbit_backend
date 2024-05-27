from typing import Tuple
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.memory.subject_repository import (
    SubjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.topic_repository import (
    TopicMemoryRepository,
)
from rabbit_backend.quiz.interactors.dtos.subject_dtos import SubjectDTO
from rabbit_backend.quiz.interactors.dtos.topic_dtos import TopicCreateDTO, TopicDTO
from rabbit_backend.quiz.interactors.subjects import (
    AddSubjectUseCase,
    PublishSubjectUseCase,
)
from rabbit_backend.quiz.interactors.topics import AddTopicUseCase
from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository


def create_dummy_topics(
    subject_repository: SubjectMemoryRepository,
    topic_repository: TopicMemoryRepository,
    user_repository: UserMemoryRepository,
    regular_user_id: UUID,
    admin_user_id: UUID,
) -> Tuple[SubjectDTO, TopicDTO, TopicDTO]:
    add_subject = AddSubjectUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    add_topic = AddTopicUseCase(
        subject_repository,
        topic_repository,
        user_repository,
    )
    publish_subject = PublishSubjectUseCase(
        subject_repository,
        user_repository,
    )
    subject = add_subject("test_subject", admin_user_id)
    publish_subject(subject.id, admin_user_id)
    subject.is_published = True
    new_topic = TopicCreateDTO(
        name="test_topic",
        question_type="test",
        user_id=admin_user_id,
        subject_id=subject.id,
    )
    topic = add_topic(new_topic)
    new_topic_2 = TopicCreateDTO(
        name="test_topic_2",
        question_type="card",
        user_id=regular_user_id,
        subject_id=subject.id,
    )
    topic2 = add_topic(new_topic_2)
    return subject, topic, topic2
