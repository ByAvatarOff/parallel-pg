import aiofiles

from typing import AsyncGenerator
from src.reader.abstract import AbstractReader
from src.core.settings import settings


class SqlReader(AbstractReader):
    async def read(self) -> AsyncGenerator[str, None]:
        async with aiofiles.open(settings.app.sql_file, "r") as file:
            read_file = await file.read()
            for line in read_file.replace('\n', " ").split(';'):
                if line:
                    yield line