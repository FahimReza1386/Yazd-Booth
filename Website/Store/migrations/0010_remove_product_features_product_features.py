# Generated by Django 5.1 on 2024-08-10 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_feature_product_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='features',
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Store.feature'),
        ),
    ]
