from django.contrib import admin 
from django.contrib.auth.models import User 
from django.db import models 
from oauth2client.contrib.django_util.models import CredentialsField 
  
  
class CredentialsModel(models.Model): 
    id = models.ForeignKey(User, primary_key = True, on_delete = models.CASCADE) 
    credential = CredentialsField() 
    task = models.CharField(max_length = 80, null = True) 
    updated_time = models.CharField(max_length = 80, null = True) 
  
class SessId(models.Model):
    session = models.CharField(max_length = 80, null = True)
    access_code = models.CharField(max_length = 80, null = True)
    #http = models.CharField(max_length = 300, null = True)
    credential = CredentialsField()
    def __str__(self):
        return self.access_code
class CredentialsAdmin(admin.ModelAdmin): 
    pass
