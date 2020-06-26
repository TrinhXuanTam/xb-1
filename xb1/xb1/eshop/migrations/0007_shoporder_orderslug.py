# Generated by Django 3.0.3 on 2020-05-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0006_auto_20200423_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoporder',
            name='orderSlug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug'),
        ),
    ]