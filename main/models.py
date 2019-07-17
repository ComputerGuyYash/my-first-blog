from django.db import models

# Create your models here.
class Wids(models.Model):
    session = models.CharField(max_length = 80, null = True)
    widgets = models.CharField(max_length = 1,null= True)
    remarks = models.CharField(max_length = 80,null= True)
class Loop(models.Model):
    session = models.CharField(max_length = 80, null = True)
    div = models.CharField(max_length = 80, null = True)
    label = models.CharField(max_length = 80, null = True)
class Pin(models.Model):
    session = models.CharField(max_length = 80, null = True)
    div = models.CharField(max_length = 80, null = True)
    label = models.CharField(max_length = 80, null = True)
class Emails(models.Model):
    session = models.CharField(max_length = 80, null = True)
    email = models.CharField(max_length = 80, null = True)
