from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, UUID4


class Video(BaseModel):
    id: UUID4
    publication_datetime: datetime
    duration: float
    year_views: int
    title: str
    description: str
    category: str


class InteractionType(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class Interaction(BaseModel):
    user_id: UUID4
    video_id: UUID4
    type: InteractionType
