from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.auth.handlers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    app = FastAPI(
        title='Auth Service',
        description='Simple JWT auth service',
        docs_url='/api/docs',
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(router, prefix='/auth')

    return app
