# Generated by Django 4.0.1 on 2022-03-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/avatar1.jpg', null=True, upload_to='avatars/%Y/%m', verbose_name='Avatar'),
        ),
    ]
