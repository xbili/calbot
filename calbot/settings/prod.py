from calbot.settings.defaults import *

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
            'filename': '/var/log/calbot/calbot.log',
            'formatter': 'verbose',
        },
        'error': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/calbot/calbot-error.log',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
