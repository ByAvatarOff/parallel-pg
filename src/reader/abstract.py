from abc import ABC, abstractmethod
from typing import AsyncGenerator


class AbstractReader(ABC):
    @abstractmethod
    async def read(self) -> AsyncGenerator[str, None]: ...
