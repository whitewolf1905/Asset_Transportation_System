from django.db import models
from rest_framework import serializers


Travel_Choice = [
    ('BUS', 'BUS'),
    ('CAR', 'CAR'),
    ('TRAIN', 'TRAIN')
]

Asset_Sensitivity = [
    ('HIGHLY_SENSITIVE', 'HIGHLY_SENSITIVE'),
    ('SENSITIVE', 'SENSITIVE'),
    ('NORMAL', 'NORMAL')
]

Asset_Type = [
    ('LAPTOP', 'LAPTOP'),
    ('TRAVEL_BAG', 'TRAVEL_BAG'),
    ('PACKAGE', 'PACKAGE')
]

# Create your models here.


class Requesters(models.Model):
    requester_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Riders(models.Model):
    rider_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class RidersTravelInfo(models.Model):
    riders_id = models.IntegerField()
    travel_from = models.CharField(max_length=100)
    travel_to = models.CharField(max_length=100)
    travel_date = models.DateField()
    travel_medium = models.CharField(
        max_length=50,
        choices=Travel_Choice,
        default='CAR'
    )
    asset_quantity = models.IntegerField(default=0)


class RidersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RidersTravelInfo
        fields = "__all__"


class RequesterHistory(models.Model):
    requester_id = models.IntegerField()
    pick_from = models.CharField(max_length=100)
    deliver_to = models.CharField(max_length=100)
    deliver_date = models.DateField()
    asset = models.IntegerField()
    asset_type = models.CharField(
        max_length=50,
        choices= Asset_Type,
        default='PACKAGE'
    )
    asset_sensitivity = models.CharField(
        max_length=50,
        choices= Asset_Sensitivity,
        default='NORMAL'
    )
    receiver = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Pending')


class RequesterHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequesterHistory
        fields = "__all__"

