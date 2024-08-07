import os
from typing import Callable
import logging.config
from src.core.settings import settings


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(settings.app.log_dir, "app.log"),
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def transaction_detail(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> None:
        logger.info("-------------transactions begin--------------")
        result = await func(*args, **kwargs)
        logger.info("-----------transactions end-----------------")
        return result
    return wrapper