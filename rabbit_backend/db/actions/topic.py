from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_backend.db.dao.topic_dao import TopicDAO
from rabbit_backend.db.exeptions import backend_exception
from rabbit_backend.db.models.topics import Topic

# TODO: аннотация типов


@backend_exception
async def _create_topic_in_db(topic_name: str, session: AsyncSession) -> Topic:
    async with session.begin():
        topic_dao = TopicDAO(session)
        return await topic_dao.create_topic(topic_name=topic_name)


@backend_exception
async def _get_topic_from_db(topic_id: UUID, session: AsyncSession) -> Topic:
    async with session.begin():
        topic_dao = TopicDAO(session)
        return await topic_dao.get_topic_by_id(topic_id=topic_id)


@backend_exception
async def _get_all_topics_from_db(session: AsyncSession) -> dict[str, str]:
    async with session.begin():
        topic_dao = TopicDAO(session)
        topics = await topic_dao.get_all_topics()
        if topics:
            return {str(topic[0]): topic[1] for topic in topics}
        return dict()


@backend_exception
async def _update_topic_name_in_db(
    topic_id: UUID,
    name: str,
    session: AsyncSession,
) -> None:
    async with session.begin():
        topic_dao = TopicDAO(session)
        await topic_dao.update_topic_name(topic_id=topic_id, name=name)
