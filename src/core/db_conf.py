from random import randint

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.logger import logger
from src.core.settings import settings

engine = create_async_engine(settings.db.async_url, echo=False)
SessionMaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class AsyncSessionFactory:
    def __init__(self) -> None:
        self.session_id = randint(100, 1000)

    async def __aenter__(self) -> SessionMaker:
        self.session = SessionMaker()
        self.session.session_id = self.session_id
        logger.info(
            f"Worker: {self.session_id} -------------transactions begin--------------",
        )
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            await self.session.commit()
            logger.info(
                f"Worker: {self.session_id}. Transaction completed",
            )
        else:
            await self.session.rollback()
            logger.error(
                f"Worker: {self.session_id}. Transaction rollback with error: {exc_value}",
            )
        await self.session.close()
        logger.info(
            f"Worker: {self.session_id} -----------transactions end-----------------",
        )
