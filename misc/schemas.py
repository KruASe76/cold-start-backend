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


class Interaction(BaseModel):
    user_id: UUID
    video_id: UUID
    type: InteractionType

    class Config:
        from_attributes = True
