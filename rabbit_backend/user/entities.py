from pydantic import UUID4, BaseModel


class User(BaseModel):
    """User Entity."""

    id: UUID4
