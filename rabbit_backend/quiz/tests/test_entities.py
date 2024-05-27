# flake8: noqa
from datetime import datetime
from uuid import uuid4

import pytest

from rabbit_backend.quiz.entities import (
    CardQuestionEntity,
    QuestionEntityFactory,
    SubjectEntity,
    TestQuestionEntity,
    TopicEntity,
)
from rabbit_backend.user.entities import UserEntity


def test_question_correct() -> None:
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    topic = TopicEntity(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        name="sdfsd",
        question_type="test",
        questions=[],
        subject=SubjectEntity(
            id=uuid4(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            name="sdfsd",
            topics=[],
        ),
    )
    q = QuestionEntityFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
        topic=topic,
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
    topic = TopicEntity(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        name="sdfsd",
        question_type="test",
        questions=[],
        subject=SubjectEntity(
            id=uuid4(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            name="sdfsd",
            topics=[],
        ),
    )
    with pytest.raises(ValueError):
        q = QuestionEntityFactory.get_question(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            data=data,  # type: ignore
            topic=topic,
        )


def test_question_card() -> None:
    data = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    topic = TopicEntity(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        name="sdfsd",
        question_type="test",
        questions=[],
        subject=SubjectEntity(
            id=uuid4(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            name="sdfsd",
            topics=[],
        ),
    )
    q = QuestionEntityFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
        topic=topic,
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
            question_type="dsfsdf",
            questions=[],
            subject=SubjectEntity(
                id=uuid4(),
                user=UserEntity(id=uuid4()),
                is_published=False,
                name="sdfsd",
                topics=[],
            ),
        )

    topic = TopicEntity(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=UserEntity(id=uuid4()),
        is_published=False,
        name="sdfsd",
        question_type="test",
        questions=[],
        subject=SubjectEntity(
            id=uuid4(),
            user=UserEntity(id=uuid4()),
            is_published=False,
            name="sdfsd",
            topics=[],
        ),
    )
