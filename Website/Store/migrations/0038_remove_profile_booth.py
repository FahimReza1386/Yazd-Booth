# Generated by Django 5.1 on 2024-08-17 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0037_alter_profile_booth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='booth',
        ),
    ]
