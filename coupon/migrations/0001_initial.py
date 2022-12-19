# Generated by Django 3.2 on 2022-12-19 00:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('use_from', models.DateTimeField()),
                ('use_to', models.DateTimeField()),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)])),
                ('active', models.BooleanField()),
            ],
        ),
    ]
