# Generated by Django 5.1 on 2024-08-18 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0048_booth_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='booth',
            name='popularity_percentage',
            field=models.FloatField(default=0),
        ),
    ]
