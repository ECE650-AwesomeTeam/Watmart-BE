from django.contrib import admin
from django.urls import path
from backbone import views

urlpatterns = [
    path('signup', views.signup, name='signup'),     # urls.py(Watmart) > urls.py(Backbone) > views.py(Backbone)
]
