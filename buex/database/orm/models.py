from django.db import models
from django.contrib.auth.models import AbstractUser

class tbl_user(AbstractUser):
    uid = models.BigIntegerField(default=0)
    s_password = models.CharField(default='', max_length=512)

class guard(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

class location(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

class attendance(models.Model):
    guard_id = models.IntegerField(default=0, blank=True)
    location_id = models.IntegerField(default=0, blank=True)
    attented_hour = models.IntegerField(default=0, blank=True)
    attended_date = models.DateField(blank=True)

class serivcecost(models.Model):
    service_name = models.CharField(max_length=255, blank=True)
    service_cost = models.FloatField(blank=True, default=2)

class equipmenttpl(models.Model):
    equipment_name = models.CharField(max_length=255, blank=True)
    equipment_alias = models.CharField(max_length=255, blank=True)
    equipment_desp = models.CharField(max_length=255, blank=True)

class equipmentcost(models.Model):
    equipmenttpl_id = models.IntegerField(default=0, blank=True)
    assigning_loc_id = models.IntegerField(default=0, blank=True)
    equipment_cost = models.FloatField(blank=True, default=0)
    purchased_count = models.IntegerField(default=0, blank=True)
    purchased_date = models.DateField(blank=True)

class incident(models.Model):
    guard_id = models.IntegerField(default=0, blank=True)
    location_id = models.IntegerField(default=0, blank=True)
    event_time = models.DateTimeField(blank=True)
    event_type = models.CharField(max_length=255, blank=True)
    event_desp = models.CharField(max_length=255, blank=True)