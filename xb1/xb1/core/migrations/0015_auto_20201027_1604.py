# Generated by Django 3.0.3 on 2020-10-27 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_merge_20200617_1913'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('is_staff_user', 'Is user a staff'),)},
        ),
    ]
