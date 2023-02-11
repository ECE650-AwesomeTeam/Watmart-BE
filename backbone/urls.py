from django.contrib import admin
from django.urls import path
from backbone import views

urlpatterns = [
    path('', views.home, name='home')    #Directs to views.py in backbone which will link it to the FE
]
