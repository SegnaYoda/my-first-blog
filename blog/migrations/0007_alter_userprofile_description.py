# Generated by Django 4.0.1 on 2022-02-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_userprofile_description_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, default='Нет описания', max_length=300, verbose_name='Описание автора'),
        ),
    ]
