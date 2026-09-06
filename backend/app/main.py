from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import exercises, health, routines
from app.config import settings
from app.services.exercise_library import ExerciseLibrary


def create_app(library: ExerciseLibrary | None = None) -> FastAPI:
    catalog = library or ExerciseLibrary(settings.database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        catalog.initialize()
        app.state.library = catalog
        yield

    app = FastAPI(title="Coach Luna API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
    for router in (health.router, exercises.router, routines.router):
        app.include_router(router)
    return app


app = create_app()
