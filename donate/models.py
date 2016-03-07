from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

# class UserClass(models.Model):

    # ACCOUNT_TYPES = (('donor', 'donor'), ('admin', 'admin'), ('ngo', 'NGO'), ('vol', 'volunteer'))

    # account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)


class Donor(models.Model):
    user = models.OneToOneField(User, related_name='donor')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.BigIntegerField()

    collection_time = models.CharField(max_length=20)


class Admin(models.Model):
    user = models.OneToOneField(User, related_name='admin')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.BigIntegerField()


class Volunteer(models.Model):
    user = models.OneToOneField(User, related_name='volunteer')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.BigIntegerField()


class NGO(models.Model):
    user = models.OneToOneField(User, related_name='ngo')
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.BigIntegerField()
    description = models.CharField(max_length=200)
    image = models.ImageField()


class Event(models.Model):
    ngo = models.ForeignKey(NGO, db_constraint=False, on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=20, default=None)
    type = models.CharField(max_length=20, default=None)


class Donation(models.Model):
    STATUS = (('donor', 'With Donor'), ('vol', 'With volunteer'), ('ngo', 'With NGO'))
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, db_constraint=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_constraint=False)

    location = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='donor')

