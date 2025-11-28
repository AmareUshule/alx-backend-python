from datetime import datetime
import os
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure the log file directory exists
        log_dir = os.path.dirname(settings.LOG_FILE_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def __call__(self, request):
        # Get the username or 'Anonymous' if not authenticated
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        # Log the request information
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Write to the log file
        with open(settings.LOG_FILE_PATH, 'a') as log_file:
            log_file.write(log_entry)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response
