# Generated by Django 3.0 on 2020-08-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(null=True, to='product.Product'),
        ),
    ]
