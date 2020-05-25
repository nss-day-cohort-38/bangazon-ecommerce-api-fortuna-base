from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=55)

    

# Every time a `User` is created, a matching `Customer`
# object will be created and attached as a one-to-one
# property
@receiver(post_save, sender=User)
def create_Customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

# Every time a `User` is saved, its matching `Customer`
# object will be saved.
@receiver(post_save, sender=User)
def save_Customer(sender, instance, **kwargs):
    instance.customer.save()