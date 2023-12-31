# Generated by Django 3.0.3 on 2020-11-23 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20201117_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='Deleted')),
                ('received', models.BooleanField(default=False, verbose_name='Received')),
                ('variableSymbol', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='VariableSymbol')),
                ('specificSymbol', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='SpecificSymbol')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Order', verbose_name='ShopOrder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
