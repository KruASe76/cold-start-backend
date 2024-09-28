from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from misc import models, schemas


async def get_videos(db: AsyncSession, video_ids: list[UUID]) -> Sequence[models.Video]:
    statement = select(models.Video).filter(models.Video.id.in_(map(str, video_ids)))

    result = await db.execute(statement)

    return result.scalars().all()


async def insert_default_interactions(
    db: AsyncSession, user_id: UUID, video_ids: list[UUID]
) -> None:
    statement = insert(models.Interaction).values(
        [models.Interaction(user_id=user_id, video_id=video_id) for video_id in video_ids]
    )

    await db.execute(statement)
    await db.commit()


async def update_interaction(db: AsyncSession, interaction: schemas.Interaction) -> None:
    statement = (
        update(models.Interaction)
        .where(
            models.Interaction.user_id == interaction.user_id,
            models.Interaction.video_id == interaction.video_id,
        )
        .values(type=interaction.type.as_int())
    )

    await db.execute(statement)
    await db.commit()


async def get_user_interactions(db: AsyncSession, user_id: UUID) -> Sequence[models.Interaction]:
    statement = select(models.Interaction).filter(models.Interaction.user_id == user_id)

    result = await db.execute(statement)

    return result.scalars().all()


async def REMOVE(db: AsyncSession) -> Sequence[UUID]:
    statement = select(models.Video.id)

    result = await db.execute(statement)

    return result.scalars().all()
