# Generated by Django 2.1.1 on 2018-10-14 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrpgtest', '0009_auto_20181014_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='possession',
            old_name='armourStats',
            new_name='armourStatsText',
        ),
        migrations.RenameField(
            model_name='possession',
            old_name='meleeStats',
            new_name='meleeStatsText',
        ),
        migrations.RenameField(
            model_name='possession',
            old_name='rangeStats',
            new_name='rangeStatsText',
        ),
    ]