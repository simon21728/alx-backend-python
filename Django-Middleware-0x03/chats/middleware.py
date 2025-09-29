# chats/middleware.py
from datetime import datetime
import os

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Path for the log file
        self.log_file_path = os.path.join(os.path.dirname(__file__), 'requests.log')
    
    def __call__(self, request):
        # Get username if authenticated, else 'Anonymous'
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log the request
        with open(self.log_file_path, 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        
        # Continue processing the request
        response = self.get_response(request)
        return response
