from fastapi import FastAPI
from src.api.routers import router
from .loader import Loader


def create_fastapi_app():
    app = FastAPI(
        lifespan=Loader().lifespan,
    )
    app.include_router(router)
    return app
