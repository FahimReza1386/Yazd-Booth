# Generated by Django 5.1 on 2024-08-10 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0013_remove_product_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.feature'),
        ),
    ]
