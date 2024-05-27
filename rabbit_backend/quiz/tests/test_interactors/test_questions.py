from uuid import UUID

import pytest

from rabbit_backend.quiz.adapters.repository.exceptions import (
    ObjectDoesNotExistError,
    QuestionTypeMismatchError,
)
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
from rabbit_backend.quiz.interactors.questions import (
    AddQuestionUseCase,
    DeleteQuestionUseCase,
    GetQuestionUseCase,
    PublishQuestionUseCase,
    UpdateQuestionDataUseCase,
)
from rabbit_backend.quiz.interactors.topics import (
    DeleteTopicUseCase,
    GetTopicUseCase,
    PublishTopicUseCase,
)
from rabbit_backend.quiz.tests.test_interactors.dummies import create_dummy_topics
from rabbit_backend.user.repository.memory.user_repository import UserMemoryRepository


def test_add_questions(
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

    add_question = AddQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    add_question(data, topic.id, admin_user_id)
    add_question(data, topic.id, admin_user_id)
    topic = get_topic(topic.id, admin_user_id)
    assert len(topic.questions) == 2
    assert topic.questions[0].data == data
    with pytest.raises(QuestionTypeMismatchError):
        add_question(data, topic2.id, admin_user_id)
    card = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    add_question(card, topic2.id, regular_user_id)
    topic = get_topic(topic2.id, regular_user_id)
    assert len(topic.questions) == 1
    assert topic.questions[0].data == card


def test_get_question_and_publish(
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
    add_question = AddQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    q1 = add_question(data, topic.id, admin_user_id)
    q2 = add_question(data, topic.id, admin_user_id)
    card = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    q3 = add_question(card, topic2.id, regular_user_id)
    q4 = add_question(card, topic2.id, regular_user_id)
    get_question = GetQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    q1_res = get_question(q1.id, admin_user_id)
    assert q1_res.data == data
    with pytest.raises(PublicObjectAccessDeniedError):
        get_question(q2.id, regular_user_id)
    publish_question = PublishQuestionUseCase(
        question_repository,
        user_repository,
    )
    publish_question(
        q1.id,
        admin_user_id,
    )
    get_question(q1.id, regular_user_id)


def test_question_update(
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
    add_question = AddQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    q1 = add_question(data, topic.id, admin_user_id)
    q2 = add_question(data, topic.id, admin_user_id)
    card = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    card1 = {
        "type": "card",
        "question": "question1",
        "answer": "answer1",
    }
    q3 = add_question(card, topic2.id, regular_user_id)
    q4 = add_question(card, topic2.id, regular_user_id)
    get_question = GetQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )

    update_question = UpdateQuestionDataUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    update_question(card1, q3.id, regular_user_id)
    assert get_question(q3.id, regular_user_id).data == card1
    publish_question = PublishQuestionUseCase(
        question_repository,
        user_repository,
    )
    publish_question(
        q1.id,
        admin_user_id,
    )
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    publish_topic = PublishTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    publish_topic(topic.id, admin_user_id)
    topic = get_topic(topic.id, regular_user_id)
    assert len(topic.questions) == 2


def test_delete_subject_with_questions_and_topics(
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
    add_question = AddQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    q1 = add_question(data, topic.id, admin_user_id)
    q2 = add_question(data, topic.id, admin_user_id)
    card = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    card1 = {
        "type": "card",
        "question": "question1",
        "answer": "answer1",
    }
    q3 = add_question(card, topic2.id, regular_user_id)
    q4 = add_question(card, topic2.id, regular_user_id)
    get_question = GetQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )

    update_question = UpdateQuestionDataUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    update_question(card1, q3.id, regular_user_id)
    publish_question = PublishQuestionUseCase(
        question_repository,
        user_repository,
    )
    publish_question(
        q1.id,
        admin_user_id,
    )
    get_topic = GetTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    publish_topic = PublishTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    publish_topic(topic.id, admin_user_id)
    topic = get_topic(topic.id, regular_user_id)
    delete_question = DeleteQuestionUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    delete_question(q3.id, regular_user_id)
    with pytest.raises(ObjectDoesNotExistError):
        get_question(q3.id, regular_user_id)
    delete_topic = DeleteTopicUseCase(
        topic_repository,
        question_repository,
        user_repository,
    )
    delete_topic(topic2.id, admin_user_id)
    with pytest.raises(ObjectDoesNotExistError):
        get_topic(topic2.id, admin_user_id)
        get_question(q4.id, admin_user_id)
