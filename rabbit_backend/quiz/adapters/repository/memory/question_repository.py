import uuid
from typing import Optional

from rabbit_backend.quiz.adapters.repository.memory.public_object_repository import (
    PublicObjectMemoryRepository,
)
from rabbit_backend.quiz.adapters.repository.protocols.question_repository import (
    QuestionRepository,
)
from rabbit_backend.quiz.entities import QuestionEntityAbstract, TopicEntity
from rabbit_backend.user.entities import UserEntity


class QuestionMemoryRepository(
    PublicObjectMemoryRepository[QuestionEntityAbstract],
    QuestionRepository,
):
    def add(self, question: QuestionEntityAbstract) -> QuestionEntityAbstract:
        question.id = uuid.uuid4()
        self._objects[question.id] = question
        return question

    def fill_topic(
        self,
        topic: TopicEntity,
        user: UserEntity,
        limit: Optional[int] = 200,
    ) -> TopicEntity:
        questions = self._filter(
            lambda question: question.topic.id == topic.id
            and question.can_user_read(
                user,
            ),
            limit=limit,
        )
        topic.questions = questions
        return topic
