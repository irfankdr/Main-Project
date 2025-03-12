"""Fest_Hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from fest_hub_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.log),
    path('logpost',views.logpost),
    path('admin_home',views.admin_home),
    path('organizer_home',views.organizer_home),
    path('college_home',views.college_home),
    path('staff_home',views.staff_home),
    path('judge_home',views.judge_home),
    path('logout',views.logout),

# ---------------------- EVENT ORGANISETR ------------------------

    path('register_eventorganiser',views.register_eventorganiser),
    path('register_eventorganiser_post',views.register_eventorganiser_post),
    path('add_college',views.add_college),
    path('add_college_post',views.add_college_post),
    path('view_college',views.view_college),
    path('edit_college/<id>',views.edit_college),
    path('edit_college_post/<id>',views.edit_college_post),
    path('delete_college/<id>',views.delete_college),
    path('add_judge',views.add_judge),
    path('add_judge_post',views.add_judge_post),
    path('view_judge',views.view_judge),
    path('edit_judge/<id>',views.edit_judge),
    path('edit_judge_post/<id>',views.edit_judge_post),
    path('delete_judge/<id>',views.delete_judge),
    path('add_event/<id>',views.add_event),
    path('add_event_post/<id>',views.add_event_post),
    path('view_event/<id>',views.view_event),
    path('edit_event/<id>',views.edit_event),
    path('edit_event_post/<id>',views.edit_event_post),
    path('delete_event/<id>',views.delete_event),
    path('add_program',views.add_program),
    path('add_program_post',views.add_program_post),
    path('view_program',views.view_program),
    path('edit_program/<id>',views.edit_program),
    path('edit_program_post/<id>',views.edit_program_post),
    path('delete_program/<id>',views.delete_program),
    path('allocate_programs/<id>',views.allocate_programs),
    path('allocate_program_post/<id>',views.allocate_program_post),


# ------------------------ ADMIN ------------------------------

    path('viewandverifyevent',views.viewandverifyevent),
    path('approve_event_organizer/<id>',views.approve_event_organizer),
    path('reject_organizer/<id>',views.reject_organizer),
    path('view_verified_event_organizer',views.view_verified_event_organizer),
    path('admin_view_program',views.admin_view_program),
    path('admin_view_judge',views.admin_view_judge),
    path('admin_view_event',views.admin_view_event),
    path('admin_view_staff',views.admin_view_staff),






# ---------------------------- COLLEGE -------------------------
    path('view_and_update_profile',views.view_and_update_profile),
    path('view_and_update_profile_post',views.view_and_update_profile_post),
    path('add_staff',views.add_staff),
    path('add_staff_post',views.add_staff_post),
    path('view_staff',views.view_staff),
    path('edit_staff/<id>',views.edit_staff),
    path('edit_staff_post/<id>',views.edit_staff_post),
    path('delete_staff/<id>',views.delete_staff),
    path('college_view_event',views.college_view_event),
    path('college_view_program',views.college_view_program),
    path('assign_works/<id>',views.assign_works),
    path('assign_work_post/<id>',views.assign_work_post),
    path('view_staff_work_status/<id>',views.view_staff_work_status),
    path('view_result/<id>',views.view_result),


# ------------------------------ STAFF -------------------------------------


    path('staff_view_and_edit_profile',views.staff_view_and_edit_profile),
    path('staff_view_and_edit_profile_post',views.staff_view_and_edit_profile_post),
    path('add_student',views.add_student),
    path('add_student_post',views.add_student_post),
    path('view_student',views.view_student),
    path('edit_student/<id>',views.edit_student),
    path('edit_student_post/<id>',views.edit_student_post),
    path('delete_student/<id>',views.delete_student),
    path('view_program_request/<id>',views.view_program_request),
    path('staff_view_assigned_work',views.staff_view_assigned_work),
    path('update_work_status/<id>',views.update_work_status),
    path('staff_view_result/<id>',views.staff_view_result),
    path('staff_view_point/<id>',views.staff_view_point),
    path('send_notification',views.send_notification),
    path('send_notification_post',views.send_notification_post),
    path('update_student_request/<id>',views.update_student_request),


# ---------------------------- JUDGE -------------------------------
    path('judge_view_and_edit_profile',views.judge_view_and_edit_profile),
    path('judge_view_and_edit_profile_post',views.judge_view_and_edit_profile_post),
    path('judge_view_assigned_work',views.judge_view_assigned_work),
    path('upload_result',views.upload_result),
    path('upload_result_post',views.upload_result_post),


# ---------------------------- STUDENT -------------------------------
    path('student_login',views.student_login),
    path('student_view_profile',views.student_view_profile),
    path('student_view_event',views.student_view_event),
    path('student_view_program',views.student_view_program),
    path('student_send_request',views.student_send_request),
    path('student_view_notification',views.student_view_notification),
    path('student_view_result',views.student_view_result),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
