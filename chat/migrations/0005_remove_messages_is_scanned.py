# Generated by Django 4.0.1 on 2022-04-02 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_messages_is_scanned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='is_scanned',
        ),
    ]
