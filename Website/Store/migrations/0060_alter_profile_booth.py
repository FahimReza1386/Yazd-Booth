# Generated by Django 5.1 on 2024-08-27 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0059_alter_booth_owner_alter_profile_booth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='booth',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.booth'),
        ),
    ]
