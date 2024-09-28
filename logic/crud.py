from typing import Sequence
from uuid import UUID

from sqlalchemy import select, Row
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import win32

from misc import models, schemas


async def get_videos(
    db: AsyncSession, video_ids: list[UUID]
) -> Sequence[models.Video]:
    statement = select(models.Video).filter(models.Video.id.in_(map(str, video_ids)))

    result = await db.execute(statement)

    return result.scalars().all()


async def insert_interaction(
    db: AsyncSession, interaction: schemas.Interaction
) -> models.Interaction:
    db_interaction = models.Interaction(**interaction.model_dump())

    statement = insert(models.Interaction).values(**interaction.model_dump())
    statement = statement.on_conflict_do_update(
        index_elements=[models.Interaction.user_id, models.Interaction.video_id],
        set_={"type": statement.excluded.type},
    )

    await db.execute(statement)
    await db.commit()

    return db_interaction


async def get_user_interactions(db: AsyncSession, user_id: UUID) -> Sequence[models.Interaction]:
    statement = select(models.Interaction).filter(models.Interaction.user_id == user_id)

    result = await db.execute(statement)

    return result.scalars().all()


async def REMOVE(db: AsyncSession) -> Sequence[UUID]:
    statement = select(models.Video.id)

    result = await db.execute(statement)

    return result.scalars().all()
