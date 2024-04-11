from typing import Any
from uuid import UUID

from sqlalchemy import Row, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.exeptions import TopicIdDoesNotExists, TopicNameIsNotUnique
from rabbit_backend.db.models.topics import Topic


class TopicDAO:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_topic(self, topic_name: str) -> Topic:
        try:
            new_topic = Topic(topic_name=topic_name)
            self._db_session.add(new_topic)
            await self._db_session.flush()
            return new_topic
        except IntegrityError:
            raise TopicNameIsNotUnique

    async def get_topic_by_id(
        self,
        topic_id: UUID,
    ) -> Topic:
        query = select(Topic).where(Topic.id == topic_id)
        res = await self._db_session.execute(query)
        topic_row = res.fetchone()
        if topic_row:
            return topic_row[0]
        else:
            raise TopicIdDoesNotExists

    async def get_all_topics(self) -> list[Row[Any]] | None:
        topics = await self._db_session.execute(select(Topic.id, Topic.topic_name))
        if topics:
            return list(topics)
        else:
            return None

    async def update_topic_name(self, topic_id: UUID, name: str) -> None:
        try:
            query = update(Topic).where(Topic.id == topic_id).values(topic_name=name)
            result = await self._db_session.execute(query)
            if result.rowcount == 0:
                raise TopicIdDoesNotExists
        except IntegrityError:
            raise TopicNameIsNotUnique
