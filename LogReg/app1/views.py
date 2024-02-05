from json import dumps
from datetime import timedelta
from django.utils import timezone

from django.db.models import Sum, Func
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, ExpressionWrapper, fields
from .forms import LogTrckFilterform, SortForm
from .models import LoginHistory


@login_required(login_url='loginpage')
def homepage(request):
    # uname = Users.objects.all().annotate(duration=ExpressionWrapper(
    #     F('logout_time') - F('date_time'),
    #     output_field=fields.DurationField())).annotate(
    # )
    global formatted_session_timer
    from datetime import datetime
    session_timer = None
    login_time_str = request.session.get('login_time')

    if login_time_str:
        login_time = datetime.fromisoformat(login_time_str)
        session_timer = timezone.now() - login_time
        # print(login_time)
        formatted_session_timer = session_timer.total_seconds()
        formatted_session_timer_u = str(session_timer).split(".")[0]
        print("---",session_timer.total_seconds())
    from django.contrib.auth.models import User

    t_users = User.objects.all().count()

    yesterday = datetime.now() - timedelta(days=1)
    print(yesterday)
    yesterday_data = LoginHistory.objects.filter(date_time__gte=yesterday).values('user__username').annotate(duration=ExpressionWrapper(
        F('logout_time') - F('date_time'),
        output_field=fields.DurationField())).annotate(total_hours=Sum('duration'))
    for entry in yesterday_data:
        entry['total_hours'] = entry['total_hours'].total_seconds() / 3600.0
    # print(yesterday_data)



    context = {
            't_users': t_users,
            'session_timer': formatted_session_timer_u,
            'mydata': dumps(formatted_session_timer),
            'yesterday_data':yesterday_data,    
    }
    print(formatted_session_timer)
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('Name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print(uname, email, pass1, pass2)
        if pass1 != pass2:
            messages.add_message(request, messages.INFO, "Password Not Matching")
            return redirect('sign')
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            print(uname, email, pass1, pass2)
            return redirect('loginpage')

        # print(uname, email, password, phone, address)

    return render(request, "register.html")


def loginp(request):
    if request.method == 'POST':
        email = request.POST.get('user1')
        pass4 = request.POST.get('pw')
        username = User.objects.filter(email=email).first()
        user = authenticate(request, username=username, password=pass4)
        # print(user)
        if user is not None:
            login(request, user)
            print('-------')
            print(list(user.login_histories.values_list())[0][0])
            print('-------')

            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, "Invalid Email or Password!!!")
            return redirect('loginpage')

    return render(request, "login.html")


def logoutpage(request):
    request.session['single_browser_session_token'] = False
    logout(request)
    return redirect('loginpage')









@login_required(login_url='loginpage')
def log_history(request):
    
    # uname = LoginHistory.objects.all().values()
    global sum, formatted_duration, hours, minutes, seconds

    import datetime
    uname = LoginHistory.objects.all().annotate(duration=ExpressionWrapper(
        F('logout_time') - F('date_time'),
        output_field=fields.DurationField())).annotate(
    )
    # uname = uname.annotate(
    #     hours=Extract(F('duration'), 'hour'),
    #     minutes=Extract(F('duration'), 'minute'),
    #     seconds=Extract(F('duration'), 'second')
    # )
    # uname = LoginHistory.objects.annotate(
    #     duration_in_seconds=ExpressionWrapper(
    #         F('logout_time') - F('date_time'),
    #         output_field=fields.DurationField()
    #     ),
    #     duration_hours=Trunc(
    #         F('duration_in_seconds'),
    #         'hour',
    #         output_field=fields.DurationField()
    #     ),
    #     duration_minutes=Trunc(
    #         F('duration_in_seconds'),
    #         'minute',
    #         output_field=fields.DurationField()
    #     ),
    #     duration_seconds=Trunc(
    #         F('duration_in_seconds'),
    #         'second',
    #         output_field=fields.DurationField()
    #     )
    # )
    # tim_for=[]
    # Assuming 'uname' is a queryset containing LoginHistory objects with the 'duration' field
    for login_history in uname:
        duration_in_hours, remainder = divmod(login_history.duration.total_seconds(), 3600)
        duration_in_minutes, duration_in_seconds = divmod(remainder, 60)

        login_history.duration_hours = int(duration_in_hours)
        login_history.duration_minutes = int(duration_in_minutes)
        login_history.duration_seconds = int(duration_in_seconds)
        # tim_for+=[[{login_history.duration_hours},{login_history.duration_minutes},{login_history.duration_seconds}]]
    # print(uname.values())
    #     print(
    #         f"Hours: {login_history.duration_hours}, Minutes: {login_history.duration_minutes}, Seconds: {login_history.duration_seconds}")
    # formatted_durations = []
    # for i in uname:
    #     total_seconds = i.duration.total_seconds()
    #     hours = int(total_seconds // 3600)
    #     minutes = int((total_seconds % 3600) // 60)
    #     seconds = int(total_seconds % 60)
    #     formatted_durations.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    # print(uname.values())

    # print(uname.values())

    # print(LoginHistory.objects.all().values())
    # lgout = sorted(list(set(LoginHistory.objects.filter(is_login=False))), key=lambda item: item.date_time)[::-1]
    # lgin = sorted(list(set(LoginHistory.objects.filter(is_login=True))), key=lambda item: item.date_time)[::-1]
    # print(lgout)
    # print(active_logins)
    # print("-------------------")
    import datetime
    # from datetime import datetime, timedelta
    # a=datetime.now()
    #
    # print(uname.values())
    # return render(request, 'log.html', {'uname': uname})

    if request.method == 'POST':
        form = LogTrckFilterform(request.POST)
        if form.is_valid():
            User_Id = request.POST.get('User_Id')
            From_Date = request.POST.get('From_Date')
            To_Date = request.POST.get('To_Date')


            if User_Id:
                uname = uname.filter(user=User_Id)
                sum = uname.filter(user=User_Id).aggregate(sum=Sum('duration'))['sum']
                for login_history in uname:
                    duration_in_hours, remainder = divmod(login_history.duration.total_seconds(), 3600)
                    duration_in_minutes, duration_in_seconds = divmod(remainder, 60)

                    login_history.duration_hours = int(duration_in_hours)
                    login_history.duration_minutes = int(duration_in_minutes)
                    login_history.duration_seconds = int(duration_in_seconds)
                if sum is not None:
                    duration_seconds = sum.total_seconds()  # Calculate hours, minutes, and seconds
                    hours, remainder = divmod(duration_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                else:
                    hours, minutes, seconds = 0, 0, 0

            elif From_Date or To_Date:

                    if From_Date == To_Date:
                        uname = uname.filter(date_time__gte=To_Date)
                        sum = uname.filter(date_time__gte=To_Date).aggregate(sum=Sum('duration'))[
                        'sum']

                    else:
                        uname = uname.filter(date_time__gte=From_Date).filter(date_time__lte=To_Date)
                        sum = uname.filter(date_time__gte=From_Date).filter(date_time__lte=To_Date).aggregate(
                            sum=Sum('duration'))[
                            'sum']
                        # print(uname.values())
                    for login_history in uname:
                        duration_in_hours, remainder = divmod(login_history.duration.total_seconds(), 3600)
                        duration_in_minutes, duration_in_seconds = divmod(remainder, 60)

                        login_history.duration_hours = int(duration_in_hours)
                        login_history.duration_minutes = int(duration_in_minutes)
                        login_history.duration_seconds = int(duration_in_seconds)
                    if sum is not None:
                        duration_seconds = sum.total_seconds()  # Calculate hours, minutes, and seconds
                        hours, remainder = divmod(duration_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                    else:
                        hours,minutes,seconds = 0,0,0




            else:
                uname = uname
                sum = 0
            sum1={"hours": int(hours), "min": int(minutes), "seconds": int(seconds)}
            context = {
                'form': form,
                'uname': uname,
                'sum': sum1,
            }
            return render(request, 'log.html', context)
        else:
            return render(request, 'log.html')
    sum = 0
    context = {
        'form': LogTrckFilterform(),
        'uname': uname,
        'sum': sum,
        # 'tim_for':tim_for
    }
    # print(uname.values())
    # username =
    # print(LoginHistory.objects.all().filter(id=175))
    return render(request, 'log.html', context)
