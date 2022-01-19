from re import search
from tkinter.filedialog import SaveAs
from django.contrib import admin

# Register your models here.

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe


class PostAdminForm(forms.ModelForm):   #редактирование контента пользвателю из сайта
    content = forms.CharField(widget=CKEditorUploadingWidget()) #переопределение поля контента из файла models(контент новости)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True      #позвоялет сохранить состояние введенной ранее новости
    save_on_top = True
    list_display = ('id', 'author', 'title', 'slug', 'category', 'created_at', 'get_photo')
    list_display_links = ('id', 'title')
    search_fileds = ('title', 'author' )
    list_filter = ('category', 'author', 'tags' )
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'author', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" >')
        return '-'
    
    get_photo.short_description = 'Фото'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)   #регистрация приложения в проекте
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

