# Generated by Django 5.1 on 2024-08-10 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_remove_product_features_product_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='features',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.feature'),
        ),
    ]
