from fastapi import Depends, APIRouter, Body
from src.transactions.schema.sql_schema import SqlSchema, IsolationLevelSchema, PostgresLockSchema
from src.transactions.depends.depends import get_transaction_Service
from src.transactions.domain.services.db_service import DBTransactionService
from src.core.settings import settings

app_router = APIRouter(
    prefix='/api',
    tags=['app']
)


@app_router.post("/execute_transactions")
async def execute_transactions(
        data: SqlSchema = Body(...),
        db_service: DBTransactionService = Depends(get_transaction_Service)
):
    await db_service.run(data=data)
    return {"data": "transactions completed"}


@app_router.post("/set_isolation_level")
async def set_isolation_level(data: IsolationLevelSchema = Body(...)):
    settings.db.isolation_level = data.isolation_level
    return {"data": "isolation level changed"}


@app_router.post("/set_lock_table")
async def set_lock_table(data: PostgresLockSchema = Body(...)):
    settings.db.enabled_lock_table = data.lock_level
    return {"data": f"lock table set to {data.lock_level}"}

