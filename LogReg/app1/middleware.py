from datetime import timedelta, datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from .models import LoginHistory


# class SingleBrowserSessionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             session_key = 'single_browser_session_token'
#             if session_key not in request.session:
#                 request.session[session_key] = True
#             elif not request.session[session_key]:
#                 return HttpResponse("Auto Logged out. Please <a href='/login/'>login</a> again.")
#         response = self.get_response(request)
#         return response


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser == False:
            time_since_last_login = timezone.now() - request.user.last_login
            print(f"Time since last login: {time_since_last_login}")

            # Ensure that the condition compares with a timedelta object
            if time_since_last_login >= timedelta(seconds=3600):
                print("Auto-logout condition met. Logging out user.")

                login_history = LoginHistory.objects.filter(user=request.user, is_auto_logged_out=False).first()
                if login_history:
                    login_history.is_auto_logged_out = True
                    login_history.save()

                print(login_history)

                logout(request)
                messages.add_message(request, messages.INFO, "Auto Logged out")
                return HttpResponseRedirect(reverse('loginpage'))

        response = self.get_response(request)
        return response
