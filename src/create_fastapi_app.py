from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from psycopg import InternalError
from src.api.routers import router
from src.exceptions.app_exception import AppException
from src.exceptions.not_found_error import NotFoundError
from src.exceptions.validation_error import ValidationError
from .loader import Loader


def register_middlewares(app: FastAPI):
    
    @app.middleware("http")
    async def _(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except NotFoundError as exc:
            return Response(
                status_code=404, content={"detail": exc.message}
            )
        except InternalError as exc:
            return Response(
                status_code=500, content={"detail": "Internal Server Error"}
            )
        except ValidationError as exc:
            return Response(
                status_code=422, content={"detail": exc.message}
            )
        except AppException as exc:
            return Response(
                status_code=500, content={"detail": exc.message}
            )
        except Exception as exc:
            return Response(
                status_code=500, content={"detail": "Internal Server Error"}
            )


def create_fastapi_app():
    app = FastAPI(
        lifespan=Loader().lifespan,
    )
    app.include_router(router)
    register_middlewares(app)
    return app
