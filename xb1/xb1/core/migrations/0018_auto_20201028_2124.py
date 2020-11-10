# Generated by Django 3.0.3 on 2020-10-28 20:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_merge_20201028_1831'),
        ('eshop', '0011_auto_20201027_2015'),
        ('core', '0017_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Article', verbose_name='Article'),
        ),
        migrations.AlterField(
            model_name='log',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Comment', verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='log',
            name='forum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Forum', verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='log',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eshop.ShopOrder', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='log',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 28, 21, 24, 32, 814611), verbose_name='Timestamp'),
        ),
    ]