# Generated by Django 3.0.3 on 2020-04-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20200421_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview_text',
            field=models.TextField(blank=True, null=True, verbose_name='Preview text'),
        ),
    ]
