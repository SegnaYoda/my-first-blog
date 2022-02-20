from re import search
from tkinter.filedialog import SaveAs
from django.contrib import admin

# Register your models here.
from django.forms import fields
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import Post, Category, Tag, UserProfile


class PostAdminForm(forms.ModelForm):   #редактирование контента пользвателю из сайта
    content = forms.CharField(label="Контент статьи", widget=CKEditorUploadingWidget()) #переопределение поля контента из файла models(контент новости)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True      #позвоялет сохранить состояние введенной ранее новости
    save_on_top = True  #дублирует панель сохранения в вверх
    list_display = ('id', 'author2', 'title', 'slug', 'category', 'created_at', 'update_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', 'category')    #отвечает за возможность редактирования поля прямо в таблице админки 
    search_fileds = ('title', 'author2' )
    list_filter = ('category', 'author2', 'tags', 'is_published')
    readonly_fields = ('views', 'created_at', 'get_photo', 'update_at')
    fields = ('title', 'slug', 'author2', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'is_published', 'created_at', 'update_at')

    def get_photo(self, obj):       #показ изображения статьи в админке
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" >')
        return '-'
    
    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class UserProfileAdminForm(forms.ModelForm):   #редактирование контента пользвателю из сайта
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}
    save_on_top = True  #дублирует панель сохранения в вверх
    list_display = ('id', 'user', 'slug', 'get_avatar', 'author', 'description') 
    list_display_links = ('id', 'user', 'get_avatar')
    search_fileds = ('user', 'author' )
    list_filter = ('author',)
    readonly_fields = ('get_avatar',) # обязательно read only режим
    fields = ('user', 'slug', 'avatar', 'get_avatar', 'author', 'description') # Указываем поля, которые нужно отобразить в административной форме при создании нового автора

    def get_avatar(self, obj):       
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" >')
        return '/static/images/avatar1.jpg'

    get_avatar.short_description = 'Аватар'


@admin.register(Comment) #альтернатива регистрации admin.site.register(Comment, CommentAdmin)
class CommentAdmin(admin.ModelAdmin):  
    save_on_top = True
    list_display = ('name', 'author', 'email', 'post', 'body', 'created_at', 'updated_at', 'moderation')  
    list_filter = ('moderation', 'author', 'created_at', 'updated_at') 
    list_display_links =  ('name', 'email')
    search_fields = ('name', 'email', 'author', 'body')


admin.site.register(Category, CategoryAdmin)   #регистрация приложения в проекте
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)