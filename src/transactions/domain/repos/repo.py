import asyncio

from sqlalchemy import text, Sequence, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_conf import AsyncSessionFactory
from src.core.logger import logger
from src.core.settings import settings
from src.transactions.schema.sql_schema import PostgresLock


class TransactionRawRepo:
    def __init__(self, session_factory: type(AsyncSessionFactory)):
        self.session_factory = session_factory

    async def set_isolation_level(self, session: AsyncSession) -> None:
        await session.connection(
            execution_options={
                "isolation_level": settings.db.isolation_level,
            },
        )

    async def set_lock_table(self, session: AsyncSession) -> None:
        if settings.db.enabled_lock_table == PostgresLock.NONE:
            return
        await session.execute(
            text(
                f"LOCK TABLE {settings.db.main_table_name} IN {settings.db.enabled_lock_table} MODE NOWAIT;",
            ),
        )

    async def get_rows(self, session: AsyncSession) -> Sequence[RowMapping]:
        record = await session.execute(
            text(
                f"select * from {settings.db.main_table_name}",
            ),
        )
        return record.mappings().all()

    async def fill_db(self, commands: list[str]) -> None:
        async with self.session_factory() as session:
            for command in commands:
                await session.execute(text(command))

    async def clear_count(self) -> None:
        async with self.session_factory() as session:
            await session.execute(
                text(
                    f"UPDATE {settings.db.main_table_name} SET count = 0 WHERE id = 1",
                ),
            )

    async def execute_transaction(self, queries: str | list[str]) -> None:
        async with self.session_factory() as session:
            await self.set_isolation_level(session=session)
            await self.set_lock_table(session=session)
            logger.info(
                f"Worker: {session.session_id}. records result before transaction {await self.get_rows(session)}",
            )
            if isinstance(queries, str):
                await session.execute(text(queries))
                await asyncio.sleep(0.2)
            else:
                for query in queries:
                    await session.execute(text(query))
            logger.info(
                f"Worker: {session.session_id}. records result are {await self.get_rows(session)}",
            )
