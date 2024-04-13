from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.dao.topic_dao import TopicDAO
from rabbit_backend.db.dependencies import get_db_session
from rabbit_backend.db.models import topics as models
from rabbit_backend.web.api.topics import schemas

router = APIRouter()


async def get_topic_dao(
    db_session: Annotated[AsyncSession, get_db_session],
) -> TopicDAO:
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


@router.post("/topics/", response_model=schemas.Topic)
async def create_topic(
    topic: schemas.TopicCreate,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    return await topic_dao.create_topic(topic.name)


@router.get("/topics/{topic_id}", response_model=schemas.TopicCreate)
async def get_topic_name(
    topic_id: UUID,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    return await topic_dao.get_topic_by_id(topic_id)


@router.get("/topics", response_model=list[schemas.Topic])
async def get_topics(
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> list[models.Topic]:
    return await topic_dao.get_all_topics()


@router.put("/topics/name", response_model=schemas.Topic)
async def update_topic_name(
    topic: schemas.Topic,
    topic_dao: TopicDAO = Depends(get_topic_dao),
) -> models.Topic:
    return await topic_dao.update_topic_name(topic.id, topic.name)
