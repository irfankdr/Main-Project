from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

class event_organizer(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)


class college(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE,default=1)
    EVENT_ORGANIZER = models.ForeignKey(event_organizer, on_delete=models.CASCADE, default=1)

class staff(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)
    COLLEGE = models.ForeignKey(college, on_delete=models.CASCADE, default=1)


class assign_work(models.Model):
    works = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    STAFF = models.ForeignKey(staff, on_delete=models.CASCADE, default=1)
    COLLEGE = models.ForeignKey(college, on_delete=models.CASCADE, default=1)




class judge(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)
    EVENT_ORGANIZER = models.ForeignKey(event_organizer, on_delete=models.CASCADE, default=1)

class event(models.Model):
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)       # ongoing,schedules,ongoing,completed
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    EVENT_ORGANIZER = models.ForeignKey(event_organizer, on_delete=models.CASCADE, default=1)
    JUDGE = models.ForeignKey(judge, on_delete=models.CASCADE, default=1)


class program(models.Model):
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    rounds = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    stage_latitude = models.CharField(max_length=100)
    stage_longitude = models.CharField(max_length=100)
    stage_no = models.CharField(max_length=100)
    EVENT_ORGANIZER = models.ForeignKey(event_organizer, on_delete=models.CASCADE, default=1)

class student(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    STAFF = models.ForeignKey(staff, on_delete=models.CASCADE, default=1)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)


class result(models.Model):
    result = models.CharField(max_length=100)
    PROGRAM = models.ForeignKey(program, on_delete=models.CASCADE, default=1)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE, default=1)
    JUDGE = models.ForeignKey(judge, on_delete=models.CASCADE, default=1)



class allocate_program(models.Model):
    PROGRAM = models.ForeignKey(program, on_delete=models.CASCADE, default=1)
    JUDGE = models.ForeignKey(judge, on_delete=models.CASCADE, default=1)




class review(models.Model):
    review = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE, default=1)

class point(models.Model):
    points = models.CharField(max_length=100)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE, default=1)



class schedule(models.Model):
    start_time = models.CharField(max_length=100)
    end_tim = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    EVENT_ORGANIZER = models.ForeignKey(event_organizer, on_delete=models.CASCADE, default=1)



class program_request(models.Model):
    status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    PROGRAM = models.ForeignKey(program, on_delete=models.CASCADE, default=1)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE, default=1)

# class assign_judge_work(models.Model):
#     works = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)
#     JUDGE = models.ForeignKey(judge, on_delete=models.CASCADE, default=1)
#     COLLEGE = models.ForeignKey(college, on_delete=models.CASCADE, default=1)

class notification(models.Model):
    notifications = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    PROGRAM = models.ForeignKey(program, on_delete=models.CASCADE, default=1)


