# Generated by Django 5.1 on 2024-08-27 11:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0061_remove_comments_dislikes_remove_comments_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like_Comment',
            new_name='LikeComment',
        ),
    ]
