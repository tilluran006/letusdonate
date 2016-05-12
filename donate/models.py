from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


# Create your models here.
class Donor(models.Model):
    user = models.OneToOneField(User, related_name='donor')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)

    collection_time = models.CharField(max_length=20) ##Not required currently

    def __str__(self):
        return str(self.user.username)


class NGO(models.Model):
    user = models.OneToOneField(User, related_name='ngo')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=40, default="static/user_uploads/default.jpg")

    def __str__(self):
        return str(self.user.username)


class Event(models.Model):
    name = models.CharField(max_length=50)
    ngo = models.ForeignKey(NGO, db_constraint=False, on_delete=models.CASCADE, related_name='event')
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    volunteers_required = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)

    def volunteers_enrolled(self):
        return self.volunteers.count()


class Volunteer(models.Model):
    user = models.OneToOneField(User, related_name='volunteer')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    pincode = models.IntegerField(default=0)
    phone = models.BigIntegerField(default=0)
    events_volunteered = models.ManyToManyField(Event, db_constraint=False, related_name="volunteers")

    def __str__(self):
        return str(self.user.username)


class Item(models.Model):
    name = models.CharField(max_length=20, default=None)
    type = models.CharField(max_length=20, default=None)

    def __str__(self):
        return str(self.name)

    def quantity(self):
        total = 0
        for element in self.item_quantity.all():
            total += element.quantity
        return total


class ItemQuantity(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_quantity")
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="item_quantity")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.quantity)


class Donation(models.Model):
    STATUS = (('donor', 'With Donor'), ('vol', 'With volunteer'), ('ngo', 'With NGO'))
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, db_constraint=False, related_name='donation')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_constraint=False, related_name='donation')
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=50)

    location = models.CharField(max_length=100)         # Address of item
    city = models.CharField(max_length=20)
    contact = models.BigIntegerField(default=0)        # Contact No
    status = models.CharField(max_length=10, choices=STATUS, default='donor')

    def __str__(self):
        return str(self.donor) + ", " + str(self.item)
