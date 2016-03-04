from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class UserClass(User):
    # ACCOUNT_TYPES = (('donor', 'donor'), ('admin', 'admin'), ('ngo', 'NGO'), ('vol', 'volunteer'))
    dob = models.DateField(auto_now=True, verbose_name="Date of Birth")
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.IntegerField()
    # account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)


class Donor(UserClass):
    collection_time = models.CharField(max_length=20)


class Admin(UserClass):
    pass


class Volunteer(UserClass):
    pass


class NGO(UserClass):
    pass


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
    status = models.CharField(max_length=10, choices=STATUS)

