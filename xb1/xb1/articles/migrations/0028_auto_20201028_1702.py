# Generated by Django 3.0.3 on 2020-10-28 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0027_auto_20201028_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.ForumCategory', verbose_name='Category'),
        ),
    ]
