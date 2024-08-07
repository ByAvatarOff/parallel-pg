from pydantic import BaseModel
from enum import StrEnum


class SqlSchema(BaseModel):
    first_sql: str
    second_sql: str


class IsolationLevel(StrEnum):
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"


class PostgresLock(StrEnum):
    ACCESS_SHARE = "ACCESS SHARE"
    REPEATABLE_READ = "ROW SHARE"
    ROW_EXCLUSIVE = "ROW EXCLUSIVE"
    SHARE_UPDATE_EXCLUSIVE = "SHARE UPDATE EXCLUSIVE"
    SHARE = "SHARE"
    SHARE_ROW_EXCLUSIVE = "SHARE ROW EXCLUSIVE"
    EXCLUSIVE = "EXCLUSIVE"
    ACCESS_EXCLUSIVE = "ACCESS EXCLUSIVE"
    NONE = "None"


class IsolationLevelSchema(BaseModel):
    isolation_level: IsolationLevel


class PostgresLockSchema(BaseModel):
    lock_level: PostgresLock