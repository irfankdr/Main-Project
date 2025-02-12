
from django.urls import path, include

from FestApp import views

urlpatterns = [
    path('',views.login),
    path('clgregister',views.clgregister),
    path('judge_home',views.judge_home),
    path('logincode',views.logincode),
    path('staff_home',views.staff_home),
]
