import uuid
from typing import Optional

from rabbit_backend.quiz.adapters.repository.memory.public_object_repository import (
    PublicObjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.topic_repository import (
    TopicRepository,
)
from rabbit_backend.quiz.entities import SubjectEntity, TopicEntity
from rabbit_backend.user.entities import UserEntity


class TopicMemoryRepository(
    PublicObjectMemoryRepository[TopicEntity],
    TopicRepository,
):
    def add(self, topic: TopicEntity) -> TopicEntity:
        topic.id = uuid.uuid4()
        self._objects[topic.id] = topic
        return topic

    def fill_subject(
        self,
        subject: SubjectEntity,
        user: UserEntity,
        limit: Optional[int] = 50,
    ) -> SubjectEntity:
        topics = self._filter(
            lambda topic: topic.subject.id == subject.id
            and topic.can_user_read(
                user,
            ),
            limit=limit,
        )
        subject.topics = topics
        return subject
