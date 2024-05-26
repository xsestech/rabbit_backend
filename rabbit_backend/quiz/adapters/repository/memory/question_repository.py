import uuid
from typing import Any, Optional
from uuid import UUID

from rabbit_backend.quiz.adapters.repository.memory.public_object_repository import (
    ChildPublicObjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.memory.topic_repository import (
    TopicMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.entities import (
    QuestionEntityAbstract,
    QuestionEntityFactory,
    TopicEntity,
)
from rabbit_backend.user.entities import UserEntity


class QuestionMemoryRepository(
    ChildPublicObjectMemoryRepository[QuestionEntityAbstract, TopicEntity],
    QuestionRepository,
):
    def __init__(self, topic_repository: TopicMemoryRepository) -> None:
        self._topic_repository = topic_repository
        super().__init__(topic_repository, "questions")

    def add(
        self,
        data: dict[str, Any],
        topic_id: UUID,
    ) -> QuestionEntityAbstract:
        question = QuestionEntityFactory.get_question(id=uuid.uuid4(), data=data)
        topic = self._topic_repository.get_by_id(topic_id)
        topic.questions.append(question)
        self._topic_repository.update(topic)
        self._objects[question.id] = question
        return question

    def fill_topic(
        self,
        topic: TopicEntity,
        user: UserEntity,
        limit: Optional[int] = 200,
    ) -> TopicEntity:
        questions = [
            question for question in topic.questions if question.can_user_read(user)
        ]
        topic.questions = questions[:limit]
        return topic
