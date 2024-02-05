import time

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from django.conf import settings
import datetime
from datetime import datetime, timedelta


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    ip = models.CharField(max_length=15, blank=True,null=True)  # save only ip, later we can get user's details from this ip address.
    user_agent = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now=True, null=True)
    is_login = models.BooleanField(default=True, null=True, blank=True)  # login or logout
    is_logged_in = models.BooleanField(default=True)
    is_auto_logged_out = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id} - {self.user} - {self.date_time} - {self.is_logged_in} - {self.ip} - {self.is_login} - {self.logout_time}"

    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    ip = get_client_ip(request)
    # login_time = datetime.date.today()
    LoginHistory.objects.create(
        user=user,
        ip=ip,
        user_agent=request.META['HTTP_USER_AGENT'],
        is_login=True
    )
    # print("---")
    # print(data.id)
    # print('----')
    # return JsonResponse({'data': data.id})
    # print(dir(data))


# def delete_old_login_histories(user):
#    if settings.LOGIN_HISTORY_DELETE_OLD:
#         today = datetime.date.today()
#
#         if settings.LOGIN_HISTORY_KEEP_DAYS:
#             days_x_ago = today - datetime.timedelta(days=settings.LOGIN_HISTORY_KEEP_DAYS)
#             print(days_x_ago)
#             objs = LoginHistory.objects.filter(date_time__lte=days_x_ago, user=user).order_by('-date_time')
#             objs.delete()
#         elif settings.LOGIN_HISTORY_KEEP_LAST:
#             objs = LoginHistory.objects.filter(user=user)\
#                     .order_by('-date_time')[:settings.LOGIN_HISTORY_KEEP_LAST]\
#                     .values_list("id", flat=True)
#             objs = LoginHistory.objects.exclude(pk__in=list(objs))
#             objs.delete()

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    # today = datetime.date.today()
    # print("------")
    # print(user.id)

    if user:
        ip = get_client_ip(request)
        # LoginHistory.objects.create(
        #     user=user,
        #     ip=ip,
        #     user_agent=request.META['HTTP_USER_AGENT'],
        #     is_logged_in=False,
        #     is_login=False
        # )
        # print('sssssss')
        # login_history = LoginHistory.objects.filter(pk)
        # print(login_history)
        id=list(user.login_histories.values_list())[0][0]
        # print('sssssss')
        LoginHistory.objects.filter(
            user=user, ip=ip, user_agent=request.META['HTTP_USER_AGENT']) \
            .update(is_logged_in=False)
        LoginHistory.objects.filter(
            user=user, ip=ip, id=id, user_agent=request.META['HTTP_USER_AGENT']) \
            .update(logout_time=datetime.now())



# adding custom methods to default User model
@property
def active_logins(self):
    """Check user's active logins"""

    active_logins = self.login_histories.filter(is_login=True)

    # print(tim)
    active_last_logins = self.login_histories.filter(is_login=False )
    active_last_logins = list(set(active_last_logins))
    active_logins = list(set(active_logins))
    return sorted(active_logins, key=lambda item: item.date_time)[::-1]


UserModel = get_user_model()
UserModel.add_to_class("active_logins", active_logins)
