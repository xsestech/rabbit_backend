from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.exceptions import (
    TopicIdDoesNotExistsError,
    TopicNameIsNotUniqueError,
)
from rabbit_backend.db.models.topics import Topic


class TopicDAO:
    """Topic Data Access Object.

    Parameters
    ----------
    db_session: AsyncSession
        The database session object.
    """

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_topic(self, topic_name: str) -> Topic:
        """Create a new topic object.

        Create a new topic object using the given topic name. Method will fail if
        the topic name is not unique.

        Parameters
        ----------
        topic_name: str
            The topic name. Should not be empty and should be unique.

        Raises
        ------
        TopicNameIsNotUniqueError
            Failed to create a new topic because the topic name is not unique.

        Returns
        -------
        Topic
            The database topic object.

        """
        try:
            new_topic = Topic(topic_name=topic_name)
            self._db_session.add(new_topic)
            await self._db_session.flush()
            await self._db_session.commit()
            await self._db_session.refresh(new_topic)
            return new_topic
        # Here we disable the WPS329 because we need to separate view and logic
        except IntegrityError:  # noqa: WPS329
            raise TopicNameIsNotUniqueError

    async def get_topic_by_id(
        self,
        topic_id: UUID,
    ) -> Topic:
        """Get a topic object by topic id.

        Get a topic object by topic id. Method will fail if the topic id does not exist.

        Parameters
        ----------
        topic_id: UUID
            The topic id.

        Raises
        ------
        TopicIdDoesNotExistsError
            Failed to get a topic because the topic id does not exist.

        Returns
        -------
        Topic
            The database topic object.
        """
        query = select(Topic).where(Topic.id == topic_id)
        res = await self._db_session.execute(query)
        topic_row = res.fetchone()
        if not topic_row:
            raise TopicIdDoesNotExistsError
        return topic_row[0]

    async def get_all_topics(self) -> list[Topic] | None:
        """Get all topics.

        Returns
        -------
        list[Row]
            The list of database topic objects.
        """
        query_result = await self._db_session.execute(
            select(Topic.id, Topic.topic_name),
        )
        topics = query_result.scalars().all()
        if not topics:
            return None
        return list(topics)

    async def update_topic_name(self, topic_id: UUID, name: str) -> Topic:
        """Update a topic name.

        Raises
        ------
        TopicNameIsNotUniqueError
            Failed to update a topic because the topic name is not unique.
        TopicIdDoesNotExistsError
            Failed to update a topic because the topic id does not exist.

        Parameters
        ----------
        topic_id : UUID
            The topic id.
        name : str
            The topic name. Should not be empty and should be unique.

        Returns
        -------
        Topic
            Updated topic object
        """
        try:
            # WPS221 false positive. This line is not complex, actually.
            query = (
                update(Topic).where(Topic.id == topic_id).values(topic_name=name)
            )  # noqa: WPS221, E501
            result = await self._db_session.execute(query)
            if result.rowcount == 0:
                raise TopicIdDoesNotExistsError
            return result.scalars().one()
        # Here we disable the WPS329 because we need to separate view and logic
        except IntegrityError:  # noqa: WPS329
            raise TopicNameIsNotUniqueError
