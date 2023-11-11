from django.contrib import admin
from django.urls import path
from VideoApp import views
urlpatterns = [
    path('', views.index),
    path('success', views.success),
]
