from django.contrib import admin
# Import other models as needed
from .models import *

# Register models for Django admin
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(MenuItem)
admin.site.register(MenuDate)
admin.site.register(StudentProfile)
