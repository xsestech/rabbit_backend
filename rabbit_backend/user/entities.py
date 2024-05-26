from pydantic import UUID4, BaseModel


class UserEntity(BaseModel):
    """User Entity."""

    id: UUID4
    is_admin: bool = False
