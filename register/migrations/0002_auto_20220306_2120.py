# Generated by Django 3.0 on 2022-03-07 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simorder',
            name='id_picture',
            field=models.ImageField(default='default.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='simorder',
            name='id_picture2',
            field=models.ImageField(default='default.jpg', upload_to='images'),
        ),
    ]
