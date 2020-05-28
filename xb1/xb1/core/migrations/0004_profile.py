# Generated by Django 3.0.3 on 2020-04-10 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_signup_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='profile_image')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('postalCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='PostalCode')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Surname')),
                ('phone', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]