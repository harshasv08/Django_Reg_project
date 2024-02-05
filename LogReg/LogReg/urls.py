from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signup,name='sign'),
    path('login/',views.loginp,name='loginpage'),
    path('home/',views.homepage,name='home'),
    path('login-history/', views.log_history, name='log'),
    path('logout/',views.logoutpage,name='logout'),
]
