from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.student_dashboard),
    path('stu_dash/', views.student_dashboard, name="MessDeck-student"),
    path('staff_dash/', views.staff_dashboard, name="MessDeck-staff"),
    path('complaints/', views.complaints, name='complaints'),
    path('item_ratings/', views.item_ratings, name='item_ratings'),
    path('submit_ratings/', views.submit_ratings, name='submit_ratings'),
    path('file-complaint/', views.file_complaint, name='file_complaint'),
    path('monthly_menu/', views.monthly_menu, name='monthly_menu'),
    path('complaint/<int:complaint_id>/mark_viewed/', views.mark_complaint_viewed, name='mark_complaint_viewed'),
    path('stu_contact/', views.stu_contact, name='stu_contact'),
    path('staff_contact/', views.staff_contact, name='staff_contact'),
    path('upload/', views.upload_menu, name='upload_menu'),

]
