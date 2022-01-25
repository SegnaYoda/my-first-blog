from django.urls import path
from .views import *
 
urlpatterns = [
    path('', indexhome, name='index-home'),
    path('home/', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    ]

    #path('test/', tests),]