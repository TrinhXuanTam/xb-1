# Generated by Django 3.0.3 on 2020-10-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_merge_20201028_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Deleted'),
        ),
    ]
