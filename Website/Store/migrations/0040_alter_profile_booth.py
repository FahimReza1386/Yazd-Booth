# Generated by Django 5.1 on 2024-08-17 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0039_profile_booth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='booth',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.booth'),
        ),
    ]
