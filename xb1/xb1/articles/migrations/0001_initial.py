# Generated by Django 3.0.3 on 2020-03-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Animal name')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Mammal'), (1, 'Fish'), (2, 'Ant')], verbose_name='Animal type')),
                ('can_swim', models.BooleanField(default=False, verbose_name='Can swim')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Note')),
            ],
        ),
    ]
