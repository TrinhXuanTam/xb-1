# Generated by Django 3.0.3 on 2020-10-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20200625_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Forum description'),
        ),
        migrations.AlterField(
            model_name='forumcategory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Category description'),
        ),
    ]