from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone

from django.shortcuts import render


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    login_time = timezone.now().isoformat()
    print("user {} logged in through page {}".format(user.username, request.META.get('HTTP_REFERER')))
    request.session['login_time'] = login_time
    # s = gmtime(login_time)
    # g = tstrftime("%Y-%m-%d %H:%M:%S", s)
    # print(g)
    # print("user {} logged in through page {}".format(user.username, request.META.get('HTTP_REFERER')))
    # request.session['login_time'] = time.timezone.now()



@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    # logout_time = timezone.now()
    # s = time.gmtime(logout_time)
    # h = time.strftime("%Y-%m-%d %H:%M:%S", s)
    # print(h)
    print('user {} logged out through page {}'.format(user.username, request.META.get('HTTP_REFERER')))

    # if 'login_time' in request.session:
    #     login_time = request.session['login_time']
    #     logout_time = timezone.now()
        # session_duration = str(logout_time - login_time)

        # Perform actions with the session duration
        # For example, you can save it in the database or print it
        # print(f"User session duration: {session_duration}")

        # Optional: Clear the login time from the session
    del request.session['login_time']
# a=logout_time-login_time
# print(a)
