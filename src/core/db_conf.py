from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.settings import settings


engine = create_async_engine(settings.db.async_url, echo=False)
SessionMaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
