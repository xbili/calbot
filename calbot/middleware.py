from time import time
from logging import getLogger

class LoggingMiddleware(object):
    def __init__(self):
        # arguably poor taste to use django's logger
        self.logger = getLogger('django.request')

    def process_request(self, request):
        request.timer = time()
        return None

    def process_response(self, request, response):
        self.logger.info(
            '[%s] %s (%.1fs)',
            response.status_code,
            request.get_full_path(),
            time() - request.timer
        )
        return response
