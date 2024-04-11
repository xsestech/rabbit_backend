from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.actions.topic import (
    _create_topic_in_db,
    _get_all_topics_from_db,
    _get_topic_from_db,
    _update_topic_name_in_db,
)
from rabbit_backend.db.dependencies import get_db_session
from rabbit_backend.db.models.topics import TopicSchema

router = APIRouter()


@router.post("/topic/")
async def create_topic(
    topic: TopicSchema,
    session: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    new_topic = await _create_topic_in_db(topic.name, session)
    return {"id": new_topic.id}


@router.get("/topic/{topic_id}")
async def get_topic_name(
    topic_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    topic = await _get_topic_from_db(topic_id, session)
    return {"name": topic.topic_name}


@router.get("/topic")
async def get_topics(session: AsyncSession = Depends(get_db_session)) -> Dict[str, str]:
    topics = await _get_all_topics_from_db(session)
    return topics


@router.put("/topic/name")
async def update_topic_name(
    topic: TopicSchema,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    await _update_topic_name_in_db(topic.id, topic.name, session)
