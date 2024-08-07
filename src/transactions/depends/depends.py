from src.transactions.domain.services.db_service import DBTransactionService


def get_transaction_Service():
    return DBTransactionService()