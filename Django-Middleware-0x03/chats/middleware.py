import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time
        current_hour = datetime.now().hour

        # Restrict access between 9 AM (09:00) and 6 PM (18:00)
        if current_hour < 9 or current_hour >= 18:
            # If the time is outside the allowed hours, return a 403 Forbidden response
            return HttpResponseForbidden("Access to the chat is restricted outside of 9 AM to 6 PM.")

        # Proceed with the request if within allowed time
        response = self.get_response(request)
        return response
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response
