
from django.urls import path, include

from FestApp import views

urlpatterns = [
    path('',views.login),
    path('clgregister',views.clgregister),
    path('judge_home',views.judge_home),
    path('logincode',views.logincode),

    path('eventorg_home',views.create_event),
    path('eventorg_home',views.create_program),
    path('eventreg',views.eventreg),
    path('clgregisterpost',views.clgregisterpost),
    path('verifyeventco',views.verifyeventco),
    path('event_co_home',views.event_co_home),
    path('manageevent',views.manageevent),
    path('addevent',views.addevent),
    path('addevent_post',views.addevent_post),


]
