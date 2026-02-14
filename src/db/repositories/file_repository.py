from src.db.models import File
from src.db.repositories.sqlalchemy_repository import SqlAlchemyRepository
import sqlalchemy as sa

class FileRepository(SqlAlchemyRepository):
    async def create(self, id: str) -> None:
        await self._session.execute(
            sa.insert(File).values(id=id, download_count=0)
        )

    async def exists(self, id: str) -> bool:
        result = await self._session.execute(
            sa.select(sa.exists(File).where(File.id == id))
        )
        return result.scalar_one()

    async def increment_download_count(self, id: str) -> None:
        await self._session.execute(
            sa.update(File)
            .values(download_count=File.download_count + 1)
            .where(File.id == id)
        )
        
