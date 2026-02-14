from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from src.db.setup import metadata

Base = declarative_base(metadata=metadata)


class File(Base):
    __tablename__ = "files"
    id: Mapped[str] = mapped_column(primary_key=True)
    download_count: Mapped[int]
    