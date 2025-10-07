import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden
from collections import defaultdict
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware that restricts access to certain actions based on user role.
    Only admins or moderators are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict certain paths, e.g., /chats/admin/
        if request.path.startswith('/chats/admin/') or request.path.startswith('/chats/manage/'):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            # Check for staff/admin roles
            if not (user.is_staff or user.is_superuser):
                return HttpResponseForbidden("You do not have permission to access this resource.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of chat messages per IP address.
    Example: max 5 messages per 1 minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of POST requests per IP
        self.ip_message_times = defaultdict(list)
        self.limit = 5        # max messages
        self.window = 60      # time window in seconds (1 minute)

    def __call__(self, request):
        # Only apply to POST requests to /chats/messages/ (sending messages)
        if request.method == "POST" and request.path.startswith('/chats/messages/'):
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps outside the time window
            self.ip_message_times[ip] = [
                ts for ts in self.ip_message_times[ip] if now - ts < self.window
            ]

            if len(self.ip_message_times[ip]) >= self.limit:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")

            # Record the new message timestamp
            self.ip_message_times[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            i

class RestrictAccessByTimeMiddleware:
    """
    Deny access to the messaging app outside allowed hours (6 AM - 9 PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict the /chats/ URLs
        if request.path.startswith('/chats/'):
            current_hour = datetime.now().hour
            # Allow only between 6 AM (6) and 9 PM (21)
            if current_hour < 6 or current_hour >= 21:
                return HttpResponseForbidden("Messaging app is accessible only between 6 AM and 9 PM.")

        response = self.get_response(request)
        return response

class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Log file in project base directory
        self.log_file = os.path.join(settings.BASE_DIR, 'requests.log')
        # Create the file if it doesn't exist
        if not os.path.exists(self.log_file):
            open(self.log_file, 'w').close()

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Append to the log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

        response = self.get_response(request)
        return response
