from uuid import UUID

from rabbit_backend.quiz.entities import QuestionEntityAbstract, TopicEntity


class ObjectDoesNotExistError(Exception):
    def __init__(self, object_id: UUID):
        super().__init__(f"Object with id {object_id} does not exist")


class QuestionTypeMismatchError(Exception):
    def __init__(self, question: QuestionEntityAbstract, topic: TopicEntity):
        super().__init__(
            f"Question type {question.type()} "
            f"does not match topic type {topic.question_type}",
        )
