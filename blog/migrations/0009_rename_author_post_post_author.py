# Generated by Django 4.0.1 on 2022-02-22 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_post_author_remove_post_author2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author_post',
            new_name='author',
        ),
    ]
