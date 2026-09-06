from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import exercises, health, media, routines
from app.config import settings
from app.services.exercise_library import ExerciseLibrary
from app.services.media_service import MediaService

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def create_app(library: ExerciseLibrary | None = None) -> FastAPI:
    catalog = library or ExerciseLibrary(settings.database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        catalog.initialize()
        app.state.library = catalog
        app.state.media_service = MediaService(catalog)
        yield

    app = FastAPI(title="Coach Luna API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
    for router in (health.router, exercises.router, media.router, routines.router):
        app.include_router(router)
    return app


app = create_app()
