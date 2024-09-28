from sqlalchemy import DateTime, Uuid, Float, Integer, String
from sqlalchemy.orm import mapped_column

from logic.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = mapped_column(Uuid, primary_key=True)
    publication_datetime = mapped_column(DateTime(timezone=True))
    duration = mapped_column(Float)
    year_views = mapped_column(Integer)
    title = mapped_column(String)
    description = mapped_column(String)
    category = mapped_column(String)


class Interaction(Base):
    __tablename__ = "interactions"

    user_id = mapped_column(Uuid, primary_key=True)
    video_id = mapped_column(Uuid, primary_key=True)
    type = mapped_column(String)
