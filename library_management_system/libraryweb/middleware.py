from django.http import HttpResponsePermanentRedirect
from django.urls import resolve
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import User
from django.contrib.auth import logout
from django.utils.timezone import now 
from datetime import datetime

import re

class CaseInsensitiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude paths starting with '/admin', '/static', '/media',
        # or containing 'LIBNum' (case-insensitive match)
        if not (
            request.path_info.startswith('/admin') or
            request.path_info.startswith('/static') or
            request.path_info.startswith('/media') or
            re.search(r'LIB\d+', request.path_info, re.IGNORECASE)
        ):
            try:
                # Resolve the path to check if it's valid
                resolved_path = resolve(request.path_info)
                if resolved_path:  # If a valid URL match is found
                    # Split the path into segments
                    segments = request.path_info.split('/')

                    # Title-case all segments except those containing LIBNum
                    title_cased_segments = [
                        segment if re.search(r'LIB\d+', segment, re.IGNORECASE) else segment.title()
                        for segment in segments
                    ]

                    # Rejoin the segments into the normalized path
                    normalized_path = '/'.join(title_cased_segments)

                    # Ensure the correct format, and check if any change is needed
                    if request.path_info != normalized_path:
                        # Redirect to the normalized path
                        return HttpResponsePermanentRedirect(normalized_path)
            except Exception:
                pass  # Ignore errors in resolving the path

        # Proceed with the view handling
        response = self.get_response(request)
        return response
    
class ActiveUserMiddleware:
    """
    Middleware to log out the user and clear the session if their `is_active` is False,
    but without flushing the session data.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and their `is_active` status
        if request.user.is_authenticated:
            if not request.user.is_active:
                logout(request)
                # Do not flush the session to preserve session data
                # Instead, you can use request.session.clear_expired() to clear expired session data
                return redirect(reverse('libraryweb:signin'))  # Redirect to login page

        response = self.get_response(request)
        return response


class InactivityLogoutMiddleware:
    """
    Middleware that logs out the user if they've been inactive for more than 5 minutes.
    It also updates the `is_active` status of the user before the session is flushed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in and if there's an active session
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            # If the user has been inactive for more than 5 minutes, log them out
            if last_activity:
                time_since_last_activity = now() - datetime.fromisoformat(last_activity)
                inactivity_limit = timedelta(minutes=5)

                if time_since_last_activity > inactivity_limit:
                    # Update the user's 'is_active' field to False before logging out
                    user = request.user
                    user.is_active = False
                    user.save()

                    # Logout the user
                    logout(request)
                    return redirect('libraryweb:signin')  # Redirect to the sign-in page or wherever appropriate

            # Update the last activity timestamp on every request
            request.session['last_activity'] = now().isoformat()

        # Proceed with the request
        response = self.get_response(request)
        return response