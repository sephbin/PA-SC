# Generated by Django 2.0.5 on 2018-06-18 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='headerimg',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
