# Generated by Django 4.0.1 on 2022-02-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/2022/02/avatar1.jpg', null=True, upload_to='avatars/%Y/%m', verbose_name='Avatar'),
        ),
    ]