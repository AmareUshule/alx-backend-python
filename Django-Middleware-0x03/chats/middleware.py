from datetime import datetime, time
import os
from django.conf import settings
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the username or 'Anonymous' if not authenticated
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        # Log the request information
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Write to the log file
        log_file_path = getattr(settings, 'LOG_FILE_PATH', 'requests.log')
        
        # Ensure directory exists
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_entry)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time
        current_time = datetime.now().time()
        
        # Define restricted hours: 9 PM (21:00) to 6 AM (06:00)
        start_restriction = time(21, 0)  # 9:00 PM
        end_restriction = time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        is_restricted = False
        
        if start_restriction < end_restriction:
            # Normal case: restriction within same day
            is_restricted = start_restriction <= current_time <= end_restriction
        else:
            # Overnight case: restriction spans midnight (9 PM to 6 AM)
            is_restricted = current_time >= start_restriction or current_time <= end_restriction
        
        # Check if the request is for a chat-related path
        # Use simple path checking as specified in requirements
        is_chat_path = any(keyword in request.path for keyword in ['/chat', '/messages', '/messaging'])
        
        # If it's a chat path during restricted hours, block access
        if is_chat_path and is_restricted:
            return HttpResponseForbidden(
                "Access to chat services is restricted between 9 PM and 6 AM. "
                "Please try again during allowed hours."
            )
        
        # Process the request normally if not restricted
        response = self.get_response(request)
        return response
