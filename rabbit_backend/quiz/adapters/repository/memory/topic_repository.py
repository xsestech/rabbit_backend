import uuid
from typing import Optional
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.memory.public_object_repository import (
    ChildPublicObjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.subject_repository import (
    SubjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.topic_repository import (
    TopicRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity, TopicEntity
from rabbit_backend.user.entities import UserEntity


class TopicMemoryRepository(
    ChildPublicObjectMemoryRepository[TopicEntity, SubjectEntity],
    TopicRepository,
):
    def __init__(self, subject_repository: SubjectMemoryRepository):
        self._subject_repository = subject_repository
        self._parent_objects: dict[UUID, UUID] = {}
        super().__init__(subject_repository, "topics")

    def add(self, subject_id: UUID, topic: TopicEntity) -> TopicEntity:
        topic.id = uuid.uuid4()
        subject = self._subject_repository.get_by_id(subject_id)
        subject.topics.append(topic)
        self._subject_repository.update(subject)
        self._objects[topic.id] = topic
        self._parent_objects[topic.id] = subject_id
        return topic

    def fill_subject(
        self,
        subject: SubjectEntity,
        user: UserEntity,
        limit: Optional[int] = 50,
    ) -> SubjectEntity:
        topics = [topic for topic in subject.topics if topic.can_user_read(user)]
        subject.topics = topics
        return subject

    def delete(self, topic_id: UUID) -> None:
        subject_id = self._parent_objects[topic_id]
        subject = self._subject_repository.get_by_id(subject_id)
        subject.topics.remove(self._objects[topic_id])
        self._subject_repository.update(subject)
        super().delete(topic_id)
