from re import search
from tkinter.filedialog import SaveAs
from django.contrib import admin

# Register your models here.

from django.utils.safestring import mark_safe
from .models import *


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'room', 'user', 'created_at', 'likes')
    list_display_links = ('id', 'text')
    search_fileds = ('user', 'text', 'room', )
    list_filter = ('user', 'created_at', 'is_scanned', 'room', 'likes')
    fields = ('text', 'room', 'is_scanned', 'likes')
    list_select_related = ['user', 'room',]    #оптмизирует запросы, создавая JOIN'ы
    
    class Meta:
        model = Messages


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'likes', 'dislikes', 'created_at')
    list_display_links = ('id', 'name', 'title') 
    search_fileds = ('name', 'title',)
    list_filter = ('created_at', 'likes', 'dislikes')
    fields = ('name', 'title', 'likes', 'dislikes', 'participants')
    

admin.site.register(Messages, MessagesAdmin)
admin.site.register(Room, RoomAdmin)
