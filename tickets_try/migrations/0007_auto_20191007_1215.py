# Generated by Django 2.2.5 on 2019-10-07 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_try', '0006_auto_20191007_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopinproduct',
            name='is_price_changed',
        ),
        migrations.RemoveField(
            model_name='shopinproduct',
            name='is_quantity_changed',
        ),
    ]
