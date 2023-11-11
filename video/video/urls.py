# from django.contrib import admin
# from django.urls import path
# from VideoApp import views
# urlpatterns = [
#     path('', views.index),
#     path('success', views.success),
# ]

from django.urls import path, include
from VideoApp.views import *

urlpatterns = [
    # path('', index),
    path('', include('VideoApp.urls'))
]