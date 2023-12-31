# Generated by Django 3.0.3 on 2020-11-15 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specificationentry',
            old_name='Specification',
            new_name='specification',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartentry',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Order', verbose_name='Order'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
