from enum import unique
from telnetlib import STATUS
from django.urls import reverse
from distutils.command.upload import upload
from django.db import models
# Create your models here.
from django.contrib.auth.models import User



from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #related_name='userprofile'
    slug = models.CharField(max_length=50, verbose_name='Url', blank=True, null=True)
    avatar = models.ImageField(upload_to ='avatars/%Y/%m', default='avatars/avatar1.jpg' ,verbose_name='Avatar', blank=True, null=True)
    author = models.CharField(max_length=100, verbose_name='Псевдоним, связан со статьями', blank=True)
    description = models.TextField(max_length=300, verbose_name= 'Описание автора', default='Нет описания', blank=True)

    def __str__(self):
        return str(self.user.username)

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
    author = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, verbose_name='Автор')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    update_at = models.DateTimeField(auto_now=True, verbose_name= 'Обновлено')  #удобно для отслеживания времени сохранения новости
    photo = models.ImageField(upload_to ='photos/%Y/%m/%d', blank=True, verbose_name= 'Фото') #blank= True - поле будет необязательным
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name= 'Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name= 'Теги')
    is_published = models.BooleanField(default= True, verbose_name= 'Опубликовано')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})      #формирование ссылки

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.title))[:50]
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post', verbose_name= 'К какой статье')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=150, verbose_name= 'Имя',  blank=True)
    email = models.EmailField(verbose_name= 'Email',  blank=True)
    body = models.TextField(max_length=400, verbose_name= 'Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderation = models.BooleanField(default=True, verbose_name= 'Модерация')

    class Meta:
        verbose_name = 'Комментарий(и)'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return 'Comment by {author} on {post}'.format(self.name, self.post)