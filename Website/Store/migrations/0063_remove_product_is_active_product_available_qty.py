# Generated by Django 5.1 on 2024-08-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0062_rename_like_comment_likecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_active',
        ),
        migrations.AddField(
            model_name='product',
            name='Available_Qty',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
