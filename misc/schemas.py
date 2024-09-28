from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Video(BaseModel):
    id: UUID
    publication_datetime: datetime
    duration: float
    year_views: int
    title: str
    description: str
    category: str

    class Config:
        from_attributes = True


class InteractionType(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"
    NONE = "none"

    def as_int(self) -> int:
        _int_map = {
            self.LIKE: 1,
            self.DISLIKE: -1,
            self.NONE: 0,
        }

        return _int_map[self]


class Interaction(BaseModel):
    user_id: UUID
    video_id: UUID
    type: InteractionType

    class Config:
        from_attributes = True
