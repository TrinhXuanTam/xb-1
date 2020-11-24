from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_payment'),
        ('core', '0020_auto_20201029_2238'),
    ]

    def forwards_func(apps, schema_editor):

        Log = apps.get_model('core','Log')
        Log.objects.update(order=None)

    operations = [
        migrations.AlterField(
            model_name='log',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Order', verbose_name='Order'),
        ),
        migrations.RunPython(forwards_func),
    ]
