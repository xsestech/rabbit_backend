from __future__ import annotations

from typing import Optional
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.exceptions import (
    TopicIdDoesNotExistsError,
    TopicNameIsNotUniqueError,
)
from rabbit_backend.db.models.topics import Topic


class TopicDAO:
    """Topic Data Access Object

    Parameters
    ----------
    db_session: AsyncSession
        The database session object.
    """

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_topic(self, topic_name: str) -> Topic:
        """Create a new topic object.

        Parameters
        ----------
        topic_name: str

        Returns
        -------
        Topic
            The database topic object.

        """
        try:
            new_topic = Topic(topic_name=topic_name)
            self._db_session.add(new_topic)
            await self._db_session.flush()
            return new_topic
        except IntegrityError:
            raise TopicNameIsNotUniqueError

    async def get_topic_by_id(
        self,
        topic_id: UUID,
    ) -> Topic:
        """Get a topic object by topic id.

        Parameters
        ----------
        topic_id: UUID

        Returns
        -------
        Topic
            The database topic object.
        """
        query = select(Topic).where(topic_id == Topic.id)
        res = await self._db_session.execute(query)
        topic_row = res.fetchone()
        if not topic_row:
            raise TopicIdDoesNotExistsError
        return topic_row[0]

    async def get_all_topics(self) -> Optional[list[Topic]]:
        """Get all topics

        Returns
        -------
        list[Row]
            The list of database topic objects."""
        query_result = await self._db_session.execute(
            select(Topic.id, Topic.topic_name),
        )
        topics = query_result.fetchall()
        if not topics:
            return None
        logger.debug(topics)
        return list(topics)

    async def update_topic_name(self, topic_id: UUID, name: str) -> Topic:
        """Update a topic name

        Parameters
        ----------
        topic_id : UUID
        name : str

        Returns
        -------
        Topic
            Updated topic object
        """
        try:
            query = update(Topic).where(topic_id == Topic.id).values(topic_name=name)
            result = await self._db_session.execute(query)
            if result.rowcount == 0:
                raise TopicIdDoesNotExistsError
            return result.fetchone()[0]
        except IntegrityError:
            raise TopicNameIsNotUniqueError
