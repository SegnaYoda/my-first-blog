# Generated by Django 4.0.1 on 2022-02-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='slug',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Url'),
        ),
    ]
