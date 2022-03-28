import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.contrib.auth.models import User
from blog.models import UserProfile



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })



class GetUser(ListView):
    model = UserProfile
    template_name = 'chat/index.html'
    context_object_name = 'user_s'

    #def get_queryset(self):
     #   return UserProfile.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Главная страница'
        return context