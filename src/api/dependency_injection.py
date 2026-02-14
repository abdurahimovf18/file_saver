from typing import Annotated
from fastapi import Depends
from src.clients.s3_client import S3Client
from src.db.setup import new_session
from src.config import settings

from src.db.unit_of_work import UnitOfWork
from src.services.file_service import FileService


async def get_uow() -> UnitOfWork:
    return UnitOfWork(new_session=new_session)


async def get_s3_client() -> S3Client:
    endpoint_url = f"http://{settings.S3_HOST}:{settings.S3_PORT}"
    bucket_name = "files"

    return S3Client(
        endpoint_url=endpoint_url,
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        bucket_name=bucket_name
    )

async def get_file_service(
        s3_client: S3Client = Depends(get_s3_client),
        uow: UnitOfWork = Depends(get_uow),
    ) -> FileService:
    return FileService(s3_client=s3_client, uow=uow)


UOW = Annotated[UnitOfWork, Depends(get_uow)]
S3_CLIENT = Annotated[S3Client, Depends(get_s3_client)]
FILE_SERVICE = Annotated[FileService, Depends(get_file_service)]
