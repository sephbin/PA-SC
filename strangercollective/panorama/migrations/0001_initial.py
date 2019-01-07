# Generated by Django 2.1.3 on 2019-01-07 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='panorama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('left_image', models.ImageField(upload_to='')),
                ('right_image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]