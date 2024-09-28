import asyncpg
from pydantic import UUID4

from misc.config import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
)
from misc.data_models import Video, Interaction


class Database:
    _connection: asyncpg.Connection | None = None

    @classmethod
    async def create(cls) -> None:
        cls._connection = await asyncpg.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )

        await cls._connection.execute(
            "CREATE TABLE IF NOT EXISTS videos "
            "(id TEXT PRIMARY KEY, publication_datetime TIMESTAMP WITH TIME ZONE, duration REAL, year_views INT, "
            "title TEXT, description TEXT, category TEXT)"
        )

        await cls._connection.execute(
            "CREATE TABLE IF NOT EXISTS interactions "
            '(user_id TEXT, video_id TEXT, "type" TEXT, PRIMARY KEY (user_id, video_id))'
        )

    @classmethod
    async def close(cls) -> None:
        await cls._connection.close()

    @classmethod
    async def fetch_videos(cls, video_ids: list[UUID4]) -> list[Video]:
        records = await cls._connection.fetch(
            "SELECT * FROM videos WHERE id = ANY($1::text[])",
            video_ids,
        )

        return [Video.model_validate(dict(record)) for record in records]

    @classmethod
    async def insert_interaction(cls, interaction: Interaction) -> None:
        await cls._connection.execute(
            'INSERT INTO interactions (user_id, video_id, "type") VALUES ($1, $2, $3) '
            'ON CONFLICT (user_id, video_id) DO UPDATE SET "type" = excluded.type',
            str(interaction.user_id), str(interaction.video_id), interaction.type,
        )

    @classmethod
    async def REMOVE(cls) -> list[UUID4]:
        records = await cls._connection.fetch("SELECT id FROM videos")

        return [record["id"] for record in records]
