# Generated by Django 3.0.3 on 2020-11-23 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='Items', verbose_name='Product image'),
        ),
    ]
