from django.db import models

# Create your models here.

class login_table(models.Model):
    username= models.CharField(max_length=20)
    password= models.CharField(max_length=20)
    type= models.CharField(max_length=20)

class eventorganizer_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    phone=models.BigIntegerField()

class event_table(models.Model):
    eventorganizer=models.ForeignKey(eventorganizer_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    phone=models.BigIntegerField()
    latitude=models.FloatField()
    longitude=models.FloatField()

class program_table(models.Model):
    event=models.ForeignKey(event_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    details=models.CharField(max_length=100)
    rules=models.CharField(max_length=100)



