from __future__ import annotations

from typing import Annotated, AsyncGenerator
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from rabbit_backend.db.dao.topic_dao import TopicDAO
from rabbit_backend.db.dependencies import get_db_session
from rabbit_backend.db.models import topics as models
from rabbit_backend.web.api.topics import schemas

router = APIRouter()


async def get_topic_dao(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AsyncGenerator[TopicDAO, None]:
    """Create and get topic DAO.

    Parameters
    ----------
    db_session: AsyncSession
        Database session dependency

    Yields
    -------
    TopicDAO
        Topic Data Access Object
    """
    yield TopicDAO(db_session)


@router.post("/", response_model=schemas.Topic)
async def create_topic(
    topic: schemas.TopicCreate,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    """Create a new topic with all the necessary information.

    - **topic_name** - The name of the topic
    """  # noqa: DAR201, DAR101
    return await topic_dao.create_topic(topic.name)


@router.get("/{topic_id}", response_model=schemas.TopicCreate)
async def get_topic_name(
    topic_id: UUID,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    """Get a topic by its id."""  # noqa: DAR201, DAR101
    return await topic_dao.get_topic_by_id(topic_id)


@router.get("/", response_model=list[schemas.Topic])
async def get_topics(
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> list[models.Topic] | Response:
    """Get all topics."""  # noqa: DAR201, DAR101
    topics = await topic_dao.get_all_topics()
    if not topics:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return topics


@router.put("/name", response_model=schemas.Topic)
async def update_topic_name(
    topic: schemas.Topic,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    """Update a topic's name."""  # noqa: DAR201, DAR101
    return await topic_dao.update_topic_name(topic.id, topic.name)
