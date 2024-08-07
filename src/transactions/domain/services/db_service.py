from sqlalchemy.ext.asyncio import AsyncSession

from src.transactions.schema.sql_schema import SqlSchema, PostgresLock
import asyncio
from sqlalchemy import text
from src.core.logger import transaction_detail
from src.core.db_conf import SessionMaker
from src.core.settings import settings
from src.core.logger import logger


class DBTransactionService:

    async def set_lock_table(self, session) -> None:
        if settings.db.enabled_lock_table == PostgresLock.NONE:
            return
        await session.execute(
            text(
                f"LOCK TABLE {settings.db.main_table_name} IN {settings.db.enabled_lock_table} MODE NOWAIT;"
            )
        )

    async def get_counter(self, session: AsyncSession) -> int:
        record = await session.execute(
            text(
                f"select {settings.db.main_table_name}.count from {settings.db.main_table_name} where id = 1"
            )
        )
        return record.first()[0]

    @transaction_detail
    async def transaction(self, query: str, transaction_id: int) -> None:
        if not query:
            return

        async with SessionMaker() as session:
            try:
                await session.connection(
                    execution_options={
                        "isolation_level": settings.db.isolation_level
                    }
                )
                await self.set_lock_table(session=session)

                record = await session.execute(text("SELECT count(*) FROM warehouse"))
                logger.info(
                    f"Worker: {transaction_id}. "
                    f"Count records on table {settings.db.main_table_name}: {record.first()[0]}"
                )
                await session.execute(text(query))
                await asyncio.sleep(0.2)
                await session.commit()
                logger.info(
                    f"Worker: {transaction_id}. Transaction completed. Count column is {await self.get_counter(session)}"
                )
            except Exception as e:
                await session.rollback()
                logger.error(f"Worker: {transaction_id}. Transaction rollback with error:  {e}")

    async def run(self, data: SqlSchema):
        tasks = [
            self.transaction(query=data.first_sql, transaction_id=1),
            self.transaction(query=data.second_sql, transaction_id=2),
        ]
        await asyncio.gather(*tasks)
