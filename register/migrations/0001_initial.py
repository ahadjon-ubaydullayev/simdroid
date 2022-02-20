# Generated by Django 3.0 on 2022-02-20 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
                ('first_name', models.CharField(max_length=64)),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('language', models.CharField(blank=True, max_length=20, null=True)),
                ('step', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Mijozlar',
            },
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': "Sovg'alar",
            },
        ),
        migrations.CreateModel(
            name='SimCardOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sim_option', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Sim karta turlari',
            },
        ),
        migrations.CreateModel(
            name='SimOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=100)),
                ('id_picture', models.ImageField(blank=True, null=True, upload_to='images')),
                ('id_picture2', models.ImageField(blank=True, null=True, upload_to='')),
                ('tel_number', models.CharField(max_length=100)),
                ('step', models.IntegerField(default=0)),
                ('active_sim', models.BooleanField(default=False)),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Gift')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Client')),
                ('sim_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.SimCardOption')),
            ],
            options={
                'verbose_name_plural': 'Buyurtmalar',
            },
        ),
    ]
