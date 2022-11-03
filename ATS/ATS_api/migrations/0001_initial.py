# Generated by Django 4.1.3 on 2022-11-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequesterHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_id', models.IntegerField()),
                ('pick_from', models.CharField(max_length=100)),
                ('deliver_to', models.CharField(max_length=100)),
                ('deliver_date', models.DateField()),
                ('asset', models.IntegerField()),
                ('asset_type', models.CharField(choices=[('L', 'LAPTOP'), ('T', 'TRAVEL_BAG'), ('P', 'PACKAGE')], default='PACKAGE', max_length=1)),
                ('asset_sensitivity', models.CharField(choices=[('H', 'HIGHLY_SENSITIVE'), ('S', 'SENSITIVE'), ('N', 'NORMAL')], default='NORMAL', max_length=1)),
                ('receiver', models.CharField(max_length=100)),
                ('status', models.CharField(default='Pending', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Requesters',
            fields=[
                ('requester_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Riders',
            fields=[
                ('rider_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RidersTravelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riders_id', models.IntegerField()),
                ('travel_from', models.CharField(max_length=100)),
                ('travel_to', models.CharField(max_length=100)),
                ('travel_date', models.DateField()),
                ('travel_medium', models.CharField(choices=[('B', 'BUS'), ('C', 'CAR'), ('T', 'TRAIN')], default='CAR', max_length=1)),
            ],
        ),
    ]