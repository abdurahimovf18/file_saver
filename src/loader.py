from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI


class Loader:
    def __init__(self) -> None:
        pass

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:  # noqa
        async with self:
            yield

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, *args: object, **kwargs: object) -> None:
        pass
