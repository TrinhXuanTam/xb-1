# Generated by Django 3.0.3 on 2020-05-30 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0007_shoporder_orderslug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporder',
            name='orderAddressStreetNumber',
        ),
        migrations.AddField(
            model_name='shoporder',
            name='orderPhone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemActive',
            field=models.BooleanField(default=True, verbose_name='Aktivovat'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemDesc',
            field=models.CharField(max_length=200, verbose_name='Detail'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemImg',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='ShopItems', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemName',
            field=models.CharField(max_length=20, verbose_name='Název produktu'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cena'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='itemType',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Top'), (1, 'Sale'), (2, 'None'), (3, 'New')], default=2, verbose_name='Typ produktu'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='orderAddressCity',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='orderAddressPostNumber',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='orderAddressStreet',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='orderFirstName',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='orderLastName',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Surname'),
        ),
    ]