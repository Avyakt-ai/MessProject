from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # For using built-in User model if needed

from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Each model corresponds to a table in the database, and each field in the model corresponds to a column in that table.
# If we want our models(tables) to be accessed by django-admin just go to admin.py and import models and register them.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # If using Django's built-in User model
    hostel = models.CharField(max_length=50, null=True)
    bits_id = models.CharField(max_length=13, null=True)
    personal_no = models.BigIntegerField(unique=True, null=True)
    bits_email = models.CharField(max_length=50, null=True)
    about_you = models.CharField(max_length=500, null=True)


    # This str is the thing which is being shown in the admin page
    def __str__(self):
        return f"{self.user.username} - {self.hostel}"


"""
We are leveraging the functionality of groups feature in django, we divide the students and staff in 2 groups by using 
builtin django-User-field in both of their models. Now we go to python shell and create users by the command,
    from django.contrib.auth.models import User, Group
    
    # Create a user account for a student
    user = User.objects.create_user(username='student_username', email='student@example.com', password='password')
    group = Group.objects.create(name='student')
    group = Group.objects.get(name='students')
    user.groups.add(group)
    user.save()
    
    # Create a user account for staff
    user = User.objects.create_user(username='staff_username', email='staff@example.com', password='password')
    staff_group = Group.objects.get(name='Staff')
    user.groups.add(staff_group)
    user.save()
now we have divided both of the users in groups having specific permissions and access.
"""

class MenuDate(models.Model):
    month_date = models.DateField(unique=True, default=timezone.now)
    breakfast_items = models.TextField(blank=True)
    lunch_items = models.TextField(blank=True)
    dinner_items = models.TextField(blank=True)


    def __str__(self):
        return self.month_date.strftime('%B %d')


class MenuItem(models.Model):
    meal = models.ForeignKey(MenuDate, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name

    def average_rating(self):
        # Calculate the average rating for this menu item
        return Feedback.objects.filter(menu_item=self).aggregate(Avg('rating'))['rating__avg']


# This feedback is just rating and this need not to be related to a students so we can remove this foreignkey
class Feedback(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)  # ForeignKey to the User model
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    date_feedback = models.DateField(default=timezone.now().date())



    def __str__(self):
        return f"Feedback for '{self.menu_item.item_name}' - Rating: {self.rating}"


class Complaint(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='complaint_images', blank=True, null=True)
    date_complaint = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)  # Adding 'status' field as BooleanField, whether our complaint is viewed or not

    def __str__(self):
        return f"{self.id} - Status: {self.status}"

    # Either we use above str or below str
    # def __str__(self):
    #     return f"{self.student.user.username} - {self.description[:20]}"
