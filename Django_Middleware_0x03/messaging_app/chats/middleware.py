from datetime import datetime
from django.conf import settings
import os

LOG_FILE = os.path.join(settings.BASE_DIR, "requests.log")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open(LOG_FILE, "a") as f:
            f.write(log_message)

        response = self.get_response(request)
        return response
