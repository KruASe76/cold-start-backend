import random
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4

from logic.database import Database
from misc.data_models import Interaction, Video


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    await Database.create()

    yield

    await Database.close()


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


@app.get("/")
async def index() -> dict[str, str]:
    return {"status": "ok"}


@app.put("/api/v1/interaction")
async def interaction(interaction: Interaction = Body()) -> Interaction:
    await Database.insert_interaction(interaction)

    return interaction


@app.post("/api/v1/recommendations")
async def recommendations(
    user_id: UUID4 = Body(embed=True),
    limit: int = Query(default=10, ge=0),
    offset: int = Query(default=0, ge=0),
) -> list[Video]:
    all_ids = await Database.REMOVE()

    recommended_video_ids = random.sample(all_ids, limit)

    recommended_videos = await Database.fetch_videos(recommended_video_ids)

    return recommended_videos
