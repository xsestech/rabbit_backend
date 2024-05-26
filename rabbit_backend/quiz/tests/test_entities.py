# flake8: noqa
from datetime import datetime
from uuid import uuid4

import pytest

from rabbit_backend.quiz.entities import (
    CardQuestionEntity,
    QuestionEntityFactory,
    TestQuestionEntity,
    TopicEntity,
)
from rabbit_backend.user.entities import UserEntity


def test_question_right() -> None:
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    q = QuestionEntityFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
    )
    print(q.data)
    assert isinstance(q, TestQuestionEntity)
    assert q.data.dict() == data


def test_question_data_type_random() -> None:
    data = {
        "type": "adfadfadsf",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    with pytest.raises(ValueError):
        q = QuestionEntityFactory.get_question(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            data=data,  # type: ignore
        )


def test_question_data_invalid_content() -> None:
    data = {
        "type": "test",
        "question": "test question",
        "answers": "sdfsdfsdf",
    }
    with pytest.raises(ValueError):
        q = QuestionEntityFactory.get_question(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            data=data,  # type: ignore
        )


def test_question_card() -> None:
    data = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    q = QuestionEntityFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
    )

    assert isinstance(q, CardQuestionEntity)
    assert q.data.dict() == data


def test_topic_create() -> None:
    with pytest.raises(ValueError):
        topic = TopicEntity(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            name="sdfsd",
            questions_type="dsfsdf",
            questions=[],
        )

    topic = TopicEntity(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        name="sdfsd",
        questions_type="test",
        questions=[],
    )
