import os
from datetime import datetime
from django.conf import settings

# Ensure the log file path exists
LOG_FILE = os.path.join(settings.BASE_DIR, "requests.log")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the username if the user is authenticated, otherwise "Anonymous"
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        # Prepare the log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Write to the log file
        with open(LOG_FILE, "a") as f:
            f.write(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        return response
