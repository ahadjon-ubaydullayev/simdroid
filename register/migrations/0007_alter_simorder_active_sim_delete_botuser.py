# Generated by Django 4.0 on 2022-01-27 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_client_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simorder',
            name='active_sim',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='BotUser',
        ),
    ]