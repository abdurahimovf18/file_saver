from typing import AsyncGenerator
from src.clients.s3_client import S3Client
from src.db.unit_of_work import UnitOfWork
from src.exceptions.not_found_error import NotFoundError


class FileService:
    def __init__(self, s3_client: S3Client, uow: UnitOfWork) -> None:
        self._s3_client = s3_client
        self._uow = uow

    async def upload_file(self, filename: str, data: bytes) -> str:
        object_name = self._s3_client.get_object_name(filename.split(".")[-1])
        async with self._uow as uow:
            await uow.files.create(id=object_name)
            await self._s3_client.upload_file(object_name=object_name, data=data)
            await uow.commit()        
        return object_name
    
    async def stream_file(self, file_id: str) -> AsyncGenerator[bytes, None]:
        async with self._uow as uow:
            if not await uow.files.exists(file_id):
                raise NotFoundError(
                    "File not found."
                )
            await self._uow.files.increment_download_count(file_id)
            await self._uow.commit()

        stream = self._s3_client.get_file_stream(file_id, 1024 * 1024)
        async for chunk in stream:
            yield chunk
