# Generated by Django 3.0.3 on 2020-05-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_merge_20200514_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumcategory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Forum description'),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_text',
            field=models.TextField(blank=True, default='Read more...', verbose_name='Preview text'),
        ),
    ]
