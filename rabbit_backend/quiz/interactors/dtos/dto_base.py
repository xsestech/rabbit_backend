from datetime import datetime

from pydantic import UUID4, BaseModel


class DTOBase(BaseModel):
    class Config:
        from_attributes = True


class PublicCreateDTOBase(DTOBase):
    user_id: UUID4


class PublicDTOBase(PublicCreateDTOBase):
    edited_at: datetime
    created_at: datetime
