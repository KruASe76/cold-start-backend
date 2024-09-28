import random
from contextlib import asynccontextmanager, AbstractAsyncContextManager
from uuid import UUID

from fastapi import FastAPI, Body, Query, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from logic import crud
from logic.database import async_session, create_database, close_database
from misc import schemas
from misc.config import MAX_DESCRIPTION_LENGTH


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    await create_database()

    yield

    await close_database()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


app = FastAPI(lifespan=lifespan)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)


router = APIRouter()


@app.get("/")
async def index() -> dict[str, str]:
    return {"status": "ok"}


@router.put("/interaction", response_model=schemas.Interaction)
async def interaction(
    interaction: schemas.Interaction = Body(), db: AsyncSession = Depends(get_db)
):
    await crud.update_interaction(db, interaction)

    return interaction


@router.post("/recommendations", response_model=list[schemas.Video])
async def recommendations(
    user_id: UUID = Body(embed=True),
    limit: int = Query(default=10, ge=0),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    all_ids = await crud.REMOVE(db)

    recommended_video_ids = random.sample(all_ids, limit)

    recommended_videos = await crud.get_videos(db, recommended_video_ids)
    await crud.insert_default_interactions(db, user_id, recommended_video_ids)

    for video in recommended_videos:
        video.description = video.description[:MAX_DESCRIPTION_LENGTH] + (
            "..." if len(video.description.strip()) > MAX_DESCRIPTION_LENGTH else ""
        )

    return recommended_videos


app.include_router(router, prefix="/api/v1")
