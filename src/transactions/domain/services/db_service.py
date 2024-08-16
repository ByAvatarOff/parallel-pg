import asyncio

from sqlalchemy.exc import DBAPIError, IntegrityError

from src.reader.abstract import AbstractReader
from src.transactions.domain.repos.repo import TransactionRawRepo
from src.transactions.schema.sql_schema import SqlSchema


class DBTransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRawRepo,
        reader: AbstractReader,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.reader = reader

    async def fill_db(self) -> str:
        try:
            queries = [sql async for sql in self.reader.read()]
            await self.transaction_repo.fill_db(commands=queries)
            return "DB successful filled"
        except IntegrityError:
            return "DB is already filled"

    async def clear_count(self) -> str:
        try:
            await self.transaction_repo.clear_count()
            return "Count column cleaned"
        except IntegrityError:
            return "DB is not filled"

    async def transaction(self, query: str) -> None:
        if not query:
            return
        if query[-1] == ";":
            query = query[:-1]
        queries = query.split(";")
        try:
            if len(queries) > 1 and queries[-1] is not None:
                return await self.transaction_repo.execute_transaction(queries=queries)
            return await self.transaction_repo.execute_transaction(queries=query)
        except DBAPIError:
            ...

    async def run(self, data: SqlSchema):
        tasks = [
            self.transaction(query=data.first_sql),
            self.transaction(query=data.second_sql),
        ]
        await asyncio.gather(*tasks)
