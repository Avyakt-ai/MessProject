from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # If using Django's built-in User model
#     hostel = models.CharField(max_length=50, null=True)
#     bits_id = models.CharField(max_length=13, null=True)
#     personal_no = models.BigIntegerField(unique=True, null=True)
#     bits_email = models.CharField(max_length=50, null=True)
#     about_you = models.CharField(max_length=500, null=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.hostel}"