"""julia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views

from julia import settings
urlpatterns = [
    path('logout',views.logout,name='logout'),
    path('home',views.home,name='home'),
    path('fetchContent',views.Content,name='Content'),
    path('fetchMail',views.mailList,name='mailList'),
    path('Calendar',views.Calendar,name='Calendar'),
    path('fetchLabels',views.getLabels,name='getLabels'),
    path('Compose',views.Compose,name='Compose'),
    path('Search',views.Search,name='Search'),
    path('Widgets',views.Widgets,name='Widgets'),
    path('AddWid',views.AddWid,name='AddWid'),
    path('GetWidgets',views.GetWid,name='GetWid'),
    path('Test',views.Test,name='Test'),
    path('DP',views.DP,name='DP'),
    path('getEmails',views.getEmails,name='getEmails'),
    path('GetContacts',views.GetContacts,name='GetContacts'),
    path('Game',views.Game,name='Game'),
    path('AddPin',views.AddPin,name='AddPin'),
    path('GetPins',views.GetPin,name='GetPin'),
    path('FindFrom',views.FindFrom,name='FindFrom'),
    path('GetNot',views.GetNot,name='GetNot'),
    path('AddNot',views.AddNots,name='AddNots'),
    path('Trash',views.Trash,name='Trash'),
    path('MUNREAD',views.MUNREAD,name='MUNREAD'),
    path('STARRED',views.STARRED,name='STARRED'),
]
