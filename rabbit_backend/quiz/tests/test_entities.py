# flake8: noqa
from datetime import datetime
from uuid import uuid4

import pytest

from rabbit_backend.quiz.entities import CardQuestion, QuestionFactory, TestQuestion
from rabbit_backend.user.entities import User


def test_question_right() -> None:
    data = {
        "type": "test",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    q = QuestionFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=User(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
    )
    print(q.data)
    assert isinstance(q, TestQuestion)
    assert q.data.dict() == data


def test_question_data_type_random() -> None:
    data = {
        "type": "adfadfadsf",
        "question": "test question",
        "answers": ["a", "b", "c"],
        "answer_idx": 0,
    }
    with pytest.raises(ValueError):
        q = QuestionFactory.get_question(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=User(id=uuid4()),
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
        q = QuestionFactory.get_question(
            id=uuid4(),
            created_at=datetime.now(),
            edited_at=datetime.now(),
            user=User(id=uuid4()),
            is_published=False,
            data=data,  # type: ignore
        )


def test_question_card() -> None:
    data = {
        "type": "card",
        "question": "question",
        "answer": "answer",
    }
    q = QuestionFactory.get_question(
        id=uuid4(),
        created_at=datetime.now(),
        edited_at=datetime.now(),
        user=User(id=uuid4()),
        is_published=False,
        data=data,  # type: ignore
    )

    assert isinstance(q, CardQuestion)
    assert q.data.dict() == data
