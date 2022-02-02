from telnetlib import STATUS
from django.urls import reverse
from distutils.command.upload import upload
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True) 
    avatar = models.ImageField(upload_to ='avatars/%Y/%m', verbose_name='Avatar', null=True, blank=True)
    author = models.CharField(max_length=100, verbose_name='Псевдоним, связан со статьями')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('userprofile', kwargs={"slug": self.slug})      #формирование ссылки
    
    class Meta:
        verbose_name = 'Автора(ов)'
        verbose_name_plural = 'Авторы статей'
        ordering = ['-user']


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})      #формирование ссылки

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})      #формирование ссылки


#Удалить author после переноса на новую базу данных!
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)
    author = models.CharField(max_length=100, verbose_name='ОШИБКА - МОЖНО НЕ ЗАПОЛНЯТЬ', default='ОШИБКА - МОЖНО НЕ ЗАПОЛНЯТЬ') 
    author2 = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, verbose_name='Автор')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    update_at = models.DateTimeField(auto_now=True, verbose_name= 'Обновлено')  #удобно для отслеживания времени сохранения новости
    photo = models.ImageField(upload_to ='photos/%Y/%m/%d', blank=True) #blank= True - поле будет необязательным
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    is_published = models.BooleanField(default= True, verbose_name= 'Опубликовано')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})      #формирование ссылки

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


'''class Comment(models.Model):  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name= 'К какой статье')  
    name = models.CharField(max_length=150, verbose_name= 'Имя')  
    email = models.EmailField(verbose_name= 'Email')
    body = models.TextField(verbose_name= 'Комментарий')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    moderation = models.BooleanField(default=True, verbose_name= 'Модерация')  
      
    class Meta:  
        ordering = ('created',)  
          
    def __str__(self):  
        return 'Comment by {} on {}'.format(self.name, self.post)'''