# Generated by Django 5.1 on 2024-08-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0031_product_comments_product_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
