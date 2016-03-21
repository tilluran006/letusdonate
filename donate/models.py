from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Donor(models.Model):
    user = models.OneToOneField(User, related_name='donor')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)

    collection_time = models.CharField(max_length=20) ##Not required currently


class Admin(models.Model):
    user = models.OneToOneField(User, related_name='admin')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)


class Volunteer(models.Model):
    user = models.OneToOneField(User, related_name='volunteer')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)


class NGO(models.Model):
    user = models.OneToOneField(User, related_name='ngo')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)
    description = models.CharField(max_length=200)
    # image = models.ImageField()


class Event(models.Model):
    ngo = models.ForeignKey(NGO, db_constraint=False, on_delete=models.CASCADE, related_name='event')
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    time = models.CharField(max_length=15)
    description = models.CharField(max_length=50)


class Item(models.Model):
    name = models.CharField(max_length=20, default=None)
    type = models.CharField(max_length=20, default=None)


class Donation(models.Model):
    STATUS = (('donor', 'With Donor'), ('vol', 'With volunteer'), ('ngo', 'With NGO'))
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, db_constraint=False, related_name='donation')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_constraint=False, related_name='donation')
    quantity = models.IntegerField(default=0)

    location = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='donor')

