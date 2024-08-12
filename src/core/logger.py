import os
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