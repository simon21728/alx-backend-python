import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict
from django.http import HttpResponseForbidden

from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")

        # Check if the user has the 'admin' or 'moderator' role
        if not (request.user.is_staff or 'moderator' in [group.name.lower() for group in request.user.groups.all()]):
            return HttpResponseForbidden("You do not have permission to access this resource.")

        # If the user has the correct role, proceed with the request
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_message_count = defaultdict(list)  # IP -> list of timestamps

    def __call__(self, request):
        # Only track POST requests (chat messages)
        if request.method == 'POST' and request.path == '/chat/':
            ip = self.get_client_ip(request)

            # Get the current time (in seconds since epoch)
            current_time = time.time()

            # Remove timestamps that are older than 60 seconds (1 minute)
            self.user_message_count[ip] = [timestamp for timestamp in self.user_message_count[ip] if current_time - timestamp < 60]

            # Check how many messages were sent in the last 60 seconds
            if len(self.user_message_count[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. You can only send 5 messages per minute.")

            # Add the current timestamp to the list
            self.user_message_count[ip].append(current_time)

        # Process the request if within limits
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Extract the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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
