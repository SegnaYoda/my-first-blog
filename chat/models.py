from django.db import models
from django.contrib.auth import get_user_model
from blog.models import UserProfile


class Room(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField(verbose_name= 'ID название')
    title = models.CharField(max_length=255, verbose_name= 'Название чата', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= 'Дата создания')
    about = models.CharField(max_length=255, blank=True, verbose_name= 'О чате')
    likes = models.PositiveIntegerField(default=0, verbose_name= 'Кол-во лайков в чате')
    dislikes = models.PositiveIntegerField(default=0, verbose_name= 'Кол-во дизлайков в чате')
    participants = models.ManyToManyField(get_user_model(), blank=True, related_name='parts', verbose_name= 'Участники')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Чат(ы)'
        verbose_name_plural = 'Чаты'
        ordering = ['-created_at']


class Messages(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    room = models.ForeignKey(Room, related_name='rooms', null=True, on_delete=models.CASCADE, verbose_name='Чат')
    text = models.CharField(max_length=500)
    user = models.ForeignKey(get_user_model(), null= True, blank=True, on_delete=models.CASCADE, verbose_name='От кого')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    is_scanned = models.ManyToManyField(UserProfile, blank=True, verbose_name='Кем просмотрено')
    likes = models.BooleanField(verbose_name= 'Лайки', default=False)

    class Meta:
        verbose_name = 'Сообщение(я)'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']

'''
class InfoMessage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    participant = models.ManyToManyField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
'''
