from sqlalchemy.orm import DeclarativeBase

from rabbit_backend.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
