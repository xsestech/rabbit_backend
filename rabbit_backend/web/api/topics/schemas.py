from pydantic import UUID4, BaseModel, Field

TOPIC_MAX_LENGTH = 50
TOPIC_MIN_LENGTH = 1


class TopicCreate(BaseModel):
    """Pydantic model for topic create request."""

    name: str = Field(min_length=TOPIC_MIN_LENGTH, max_length=TOPIC_MAX_LENGTH)


class Topic(TopicCreate):
    """Pydantic model for topic."""

    id: UUID4

    class Config:
        from_attributes = True
