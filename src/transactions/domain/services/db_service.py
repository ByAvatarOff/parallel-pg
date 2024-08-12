from sqlalchemy.exc import IntegrityError, DBAPIError

from src.transactions.schema.sql_schema import SqlSchema
import asyncio
from sqlalchemy import text
from src.core.db_conf import AsyncSessionFactory
from src.transactions.domain.repos.repo import TransactionRawRepo
from src.reader.abstract import AbstractReader


class DBTransactionService:
    def __init__(
            self,
            transaction_repo: TransactionRawRepo,
            reader: AbstractReader
    ) -> None:
        self.transaction_repo = transaction_repo
        self.reader = reader

    async def fill_db(self) -> str:
        try:
            async for sql in self.reader.read():
                await self.transaction_repo.fill_db(command=sql)
            return "DB successful filled"
        except IntegrityError:
            return "DB is already filled"


    async def transaction(self, query: str) -> None:
        if not query:
            return
        try:
            await self.transaction_repo.execute_transaction(query=query)
        except DBAPIError: ...

    async def run(self, data: SqlSchema):
        tasks = [
            self.transaction(query=data.first_sql),
            self.transaction(query=data.second_sql),
        ]
        await asyncio.gather(*tasks)
