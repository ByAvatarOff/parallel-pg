from src.core.db_conf import AsyncSessionFactory
from src.reader.sql_reader import SqlReader
from src.transactions.domain.repos.repo import TransactionRawRepo
from src.transactions.domain.services.db_service import DBTransactionService


def get_transaction_repo():
    session_factory = AsyncSessionFactory
    return TransactionRawRepo(
        session_factory=session_factory,
    )


def get_sql_reader():
    return SqlReader()


def get_transaction_Service():
    transaction_repo = get_transaction_repo()
    reader = get_sql_reader()
    return DBTransactionService(
        transaction_repo=transaction_repo,
        reader=reader,
    )
