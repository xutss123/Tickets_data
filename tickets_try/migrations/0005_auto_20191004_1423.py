# Generated by Django 2.2.5 on 2019-10-04 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_try', '0004_auto_20191002_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='product',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='reservation',
        ),
        migrations.AddField(
            model_name='event',
            name='is_in_messenger',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_payment_partial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='shop',
            name='is_in_messenger',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='is_payment_partial',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='venue',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shopinproduct',
            name='quantity',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
