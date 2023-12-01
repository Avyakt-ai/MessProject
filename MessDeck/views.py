from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import UploadMenuForm

# By adi for showing current menu on student_dashboard
import os
import json
from datetime import date, time
from django.utils import timezone


# For complaint as viewed by staff
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect


# For complaint submitted by students
from .forms import ComplaintForm


# For uploading menu excel file
import json
from datetime import datetime
import pandas as pd
import json


@login_required
def student_dashboard(request):
    # Below 2 lines are to load the json file since it was not loading by with open("name") directly
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.abspath(os.path.join(current_dir, '..', 'Mess Menu Sample.json'))

    current_date1 = date.today().strftime('%Y-%m-%d')

    # Loading the json file to read it
    with open(json_file_path, 'r') as f:
        menu_data = json.load(f)
    current_date = date.today().strftime('%Y-%m-%d')#  Current date in date format
    current_menu1 = menu_data.get(current_date)

    # Below two lines are just to show that date and day below "Today's Menu" division
    menu_items = MenuItem.objects.all()


    # Logic to show next meal
    breakfast_time = False
    lunch_time = False
    dinner_time = False
    mess_closed = False
    message = "Mess Is Closed"
    current_time = datetime.now().time()
    if time(7,0) <= current_time <= time(9,0):
        breakfast_time = True
    elif time(12,0) <= current_time <= time(14,0):
        lunch_time = True
    elif time(18,0) <= current_time <= time(21,0):
        dinner_time = True
    else:
        mess_closed = True


    return render(request, 'MessDeck/student_dashboard.html', {
        'menu_items': menu_items,
        'current_menu1': current_menu1,
        'current_date': current_date,
        'current_date1': current_date1,
        'breakfast_time': breakfast_time,
        'lunch_time': lunch_time,
        'dinner_time': dinner_time,
        'mess_closed': mess_closed,
        'message': message,
    })

@login_required
def staff_dashboard(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'MessDeck/staff_dashboard.html',{
        'menu_items': menu_items
    })


@login_required()
def complaints(request):
    all_feedback = Feedback.objects.all()
    all_complaint = Complaint.objects.all()
    return render(request, 'MessDeck/complaints.html', {
        'all_feedback': all_feedback,
        'all_complaint': all_complaint,
    })

@login_required()

def item_ratings(request):
    # menu_items = MenuItem.objects.all()
    #
    # # Create a dictionary to store MenuItem objects and their average ratings
    # menu_item_ratings = {}
    # for item in menu_items:
    #     average = item.average_rating()  # Calculate the average rating for each menu item
    #     menu_item_ratings[item] = average if average else 0  # Set default value if no rating exists
    # return render(request, 'MessDeck/item_ratings.html', {'menu_item_ratings': menu_item_ratings})


    # Below code is when items are sorted and above code was for unsorted items.
    # Annotate each MenuItem object with its average rating
    menu_items = MenuItem.objects.annotate(avg_rating=Avg('feedback__rating'))

    # Sort the menu items by their average rating (descending order)
    menu_items_sorted = menu_items.order_by('-avg_rating')

    return render(request, 'MessDeck/item_ratings.html', {'menu_items': menu_items_sorted})


@login_required()
def mark_complaint_viewed(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    complaint.status = True
    complaint.save()
    return HttpResponseRedirect(reverse('complaints'))


# The whole below code is for submitting ratings only once and so that a student can't submit the rating multiple times in single day.
@login_required
def submit_ratings(request):
    if request.method == 'POST':
        current_user = request.user  # Get the currently authenticated user
        current_date = timezone.now().date()

        for key, value in request.POST.items():
            if key.startswith('rating_'):
                menu_item_id = key.split('_')[1]
                try:
                    menu_item = MenuItem.objects.get(pk=menu_item_id)
                    existing_feedback = Feedback.objects.filter(
                        menu_item=menu_item,
                        date_feedback=current_date,
                        student=current_user
                    ).first()

                    rating = int(value)

                    if existing_feedback:
                        # Update existing feedback if it's for the same student, menu item, and date
                        existing_feedback.rating = rating
                        existing_feedback.save()
                    else:
                        # Create new feedback if no previous rating exists for the same student, menu item, and date
                        Feedback.objects.create(menu_item=menu_item, rating=rating, student=current_user,
                                                date_feedback=current_date)

                except (MenuItem.DoesNotExist, ValueError):
                    pass  # Handle exceptions or logging here if needed

    return redirect('MessDeck-student')  # Redirect back to the student dashboard after ratings submission


# The previous code in which a student can rate infinite times.
# @login_required
# def submit_ratings(request):
#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             if key.startswith('rating_'):
#                 menu_item_id = key.split('_')[1]
#                 try:
#                     menu_item = MenuItem.objects.get(pk=menu_item_id)
#                     rating = int(value)
#                     Feedback.objects.create(menu_item=menu_item, rating=rating)
#                 except (MenuItem.DoesNotExist, ValueError):
#                     pass  # Handle exceptions or logging here if needed
#     return redirect('student_dashboard')  # Redirect back to the student dashboard after ratings submission


# Other views for authentication, complaint submission, etc.


@login_required()
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user  # Assign the logged-in user as the student
            complaint.save()
            return redirect('file_complaint')  # Redirect to the complaint page or another desired page
    else:
        form = ComplaintForm()

    return render(request, 'MessDeck/file_complaint.html', {'form': form})



def monthly_menu(request):
    menu_dates = MenuDate.objects.all()

    return render(request, 'MessDeck/monthly_menu.html', {'menu_dates': menu_dates})


def stu_contact(request):
    return render(request, 'MessDeck/stu_contact.html')

def staff_contact(request):
    return render(request, 'MessDeck/staff_contact.html')



def upload_menu(request):
    if request.method == 'POST':
        form = UploadMenuForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']

            # The Task script used to convert excel into json
            mf = pd.read_excel(excel_file, header=1)
            day = {}
            final = {}
            mf = mf.replace(r'^\*+', '', regex=True).replace('', pd.NA)
            mf = mf.apply(lambda x: x.str.upper())
            for col in mf.columns:
                breakfast_idx = mf.loc[mf[col] == "BREAKFAST"].index
                lunch_idx = mf.loc[mf[col] == "LUNCH"].index
                dinner_idx = mf.loc[mf[col] == "DINNER"].index
                ls_b = mf.loc[breakfast_idx[0] + 1: lunch_idx[0] - 2, col].dropna().tolist()
                ls_l = mf.loc[lunch_idx[0] + 1: dinner_idx[0] - 2, col].dropna().tolist()
                ls_d = mf.loc[dinner_idx[0] + 1:, col].dropna().tolist()
                day["BREAKFAST"] = ls_b
                day["LUNCH"] = ls_l
                day["DINNER"] = ls_d
                final[
                    col.strftime('%Y-%m-%d')] = day

                day = {}
            with open('Mess Menu Sample.json', 'w') as json_file:
                json.dump(final, json_file, indent=4)

            file_path = 'Mess Menu Sample.json'


            # The Below snippet is for loading menu to the models
            with open(file_path, 'r') as file:
                data = json.load(file)

                for date_str, meals in data.items():
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    menu_date, created = MenuDate.objects.get_or_create(month_date=date_obj)

                    if 'BREAKFAST' in meals:
                        menu_date.breakfast_items = ', '.join(meals['BREAKFAST'])

                    if 'LUNCH' in meals:
                        menu_date.lunch_items = ', '.join(meals['LUNCH'])

                    if 'DINNER' in meals:
                        menu_date.dinner_items = ', '.join(meals['DINNER'])

                    menu_date.save()

            return render(request, 'MessDeck/upload_menu.html')  # Redirect to a success page
    else:
        form = UploadMenuForm()
    return render(request, 'MessDeck/upload_menu.html', {'form': form})

