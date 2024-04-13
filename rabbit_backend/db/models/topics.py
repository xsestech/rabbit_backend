import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from rabbit_backend.db.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_name = Column(String, nullable=False, unique=True)
