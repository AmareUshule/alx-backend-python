from datetime import datetime, time, timedelta
import os
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse

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
class OffensiveLanguageMiddleware:
    """
    Middleware to limit chat messages per IP address.
    Users can send up to 5 messages per minute.
    """

    # Maximum messages allowed per window
    MAX_MESSAGES = 5
    # Time window in seconds
    TIME_WINDOW = 60

    def __init__(self, get_response):
        self.get_response = get_response
        # Store message timestamps by IP
        self.ip_message_log = {}

    def __call__(self, request):
        # Only track POST requests to messages endpoint
        if request.method == "POST" and request.path.startswith("/api/messages"):
            # Get client IP
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list if IP not in log
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Remove timestamps older than TIME_WINDOW
            self.ip_message_log[ip] = [
                timestamp for timestamp in self.ip_message_log[ip]
                if now - timestamp < timedelta(seconds=self.TIME_WINDOW)
            ]

            # Check if limit exceeded
            if len(self.ip_message_log[ip]) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again later."},
                    status=429
                )

            # Record current message timestamp
            self.ip_message_log[ip].append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Return the real IP of the client."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define admin/moderator actions that require special permissions
        admin_actions = ['delete', 'edit', 'moderate', 'ban', 'create_room']
        moderator_actions = ['delete', 'edit', 'moderate']
        
        # Check if the request is for a protected action
        is_protected_action = any(action in request.path.lower() for action in admin_actions)
        
        # If it's a protected action, check user role
        if is_protected_action and request.user.is_authenticated:
            # Get user role (assuming user model has a 'role' field)
            user_role = getattr(request.user, 'role', 'user').lower()
            
            # Check if user has required permissions
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden(
                    "You don't have permission to perform this action. "
                    "Admin or Moderator role required."
                )
        
        # Process the request normally if user has permission or action doesn't require it
        response = self.get_response(request)
        return response



