# Generated by Django 5.1 on 2024-08-17 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0040_alter_profile_booth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='booth',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Store.booth'),
        ),
    ]
