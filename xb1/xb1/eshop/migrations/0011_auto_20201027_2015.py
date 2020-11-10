# Generated by Django 3.0.3 on 2020-10-27 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0010_auto_20201013_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopitem',
            name='itemType',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Top'), (1, 'Sale'), (2, 'None'), (3, 'New'), (4, 'Discount')], default=2, verbose_name='Product type'),
        ),
    ]