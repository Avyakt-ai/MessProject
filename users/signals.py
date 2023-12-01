from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import StaffProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)
"""
OBJECTIVE: When we create a user through the registration form in our website then it does not create any StaffProfile 
so we cannot view any type of profile pic or anything related to StaffProfile model. so we are trying to create a
StaffProfile automatically when we create a user through our registration page in our website.

EXPLAINATION: First we have a sender(User) and a signal of post_save and this signal is recieved by this @reciever and
this signal is taken by this create_profile function and sent inside as arguments defined in this function and if that 
argument is "created" then that request goes to the model StaffProfile and it creates a profile for our registered user.
"""

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.staffprofile.save()

# now that we have a function to create profile we can also create a function to save profile.
