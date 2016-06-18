from calbot.settings import *

# Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s][%(funcName)s] %(message)s'
        },
    },
    'handlers': {
        'all': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/calbot.log',
            'formatter': 'verbose',
        },
        'error': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/calbot-error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['all', 'error'],
            'level': 'INFO',
            'propogate': True,
        },
    },
}
