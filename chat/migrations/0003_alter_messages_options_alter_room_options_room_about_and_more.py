# Generated by Django 4.0.1 on 2022-04-01 16:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_room_messages_room'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ['-created_at'], 'verbose_name': 'Сообщение(я)', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created_at'], 'verbose_name': 'Чат(ы)', 'verbose_name_plural': 'Чаты'},
        ),
        migrations.AddField(
            model_name='room',
            name='about',
            field=models.CharField(blank=True, max_length=255, verbose_name='О чате'),
        ),
        migrations.AddField(
            model_name='room',
            name='dislikes',
            field=models.PositiveIntegerField(default=0, verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='room',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Лайки'),
        ),
        migrations.AddField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='parts', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='room',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Название чата'),
        ),
        migrations.AlterField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.TextField(verbose_name='ID название'),
        ),
    ]
