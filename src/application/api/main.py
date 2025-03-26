from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.auth.handlers import router
from settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    app = FastAPI(
        title='Auth Service',
        description='Simple JWT auth service',
        docs_url='/api/docs',
        debug=settings.AUTH_SERVICE_DEBUG,
        lifespan=lifespan,
    )
    app.include_router(router, prefix='/auth')

    return app
