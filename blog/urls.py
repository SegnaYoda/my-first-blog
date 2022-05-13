from django.urls import path

from blog.feeds import LatestPostsFeed
from .views import *

#from django.contrib.auth 

 
urlpatterns = [
    path('', indexhome, name='index-home'),
    path('home/', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('feed/rss', LatestPostsFeed(), name='post_feed'),      #RSS parsing
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-post/', add_post, name='add_post'), 
    path('personalaccount/', personalaccount, name='personalaccount'), 
    path('personalaccount/contacts/', Contacts.as_view(), name='contacts'), 
    path('rssfeed/', rssfeed, name='rssfeed'), 
    ]