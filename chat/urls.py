from django.urls import path

from . import views
from .views import *


urlpatterns = [
    #path('', views.get_user_4msg, name='index_chat'),
    path('', GetUser.as_view(), name='index_chat'),
    path('<str:room_name>/', views.room, name='room'),
]