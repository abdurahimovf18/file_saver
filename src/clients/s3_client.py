import secrets
import string
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session


class S3Client:
    _OBJECT_NAME_ALLOWED_LETTERS = string.ascii_letters

    def __init__(
            self,
            endpoint_url: str, 
            access_key: str, 
            secret_key: str,
            bucket_name: str,
        ) -> None:
        self._config: dict[str, object] = {
            "endpoint_url": endpoint_url,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        self._bucket_name = bucket_name
        self._session = get_session()

    async def _setup_bucket(self, client: AioBaseClient) -> None:
        response = await client.list_buckets()  # type: ignore
        existing_buckets = [b['Name'] for b in response['Buckets']]
        if self._bucket_name not in existing_buckets:
            await client.create_bucket(Bucket=self._bucket_name)  # type: ignore

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[AioBaseClient, None]:
        async with self._session.create_client("s3", **self._config) as client:
            yield client

    async def upload_file(self, object_name: str, data: bytes) -> None:
        async with self._get_client() as client:
            await self._setup_bucket(client)
            await client.put_object(  # type: ignore
                Bucket=self._bucket_name,
                Key=object_name,
                Body=data
            )
    
    async def get_file_stream(
            self, 
            object_name: str, 
            chunk_size: int
        ) -> AsyncGenerator[bytes, None]:

        async with self._get_client() as client:
            await self._setup_bucket(client)
            response = await client.get_object(  # type: ignore
                Bucket=self._bucket_name, Key=object_name
            )
            stream = response["Body"]
            while True:
                chunk = await stream.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def get_object_name(self, ext: str) -> str:
        name = "".join(secrets.choice(self._OBJECT_NAME_ALLOWED_LETTERS) for _ in range(6))
        return f"{name}.{ext}"
