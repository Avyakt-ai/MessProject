from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, StaffUpdateForm, StaffProfileUpdateForm
from django.contrib.auth.decorators import login_required

# For custom login view
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


def register(request):
    # When we create a form it is sent as a POST request.
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login')
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required  # This is a decorator which adds a functionality to a function
def staffprofile(request):
    if request.method == "POST":
        staff_form = StaffUpdateForm(request.POST, instance=request.user)
        staff_profile_form = StaffProfileUpdateForm(request.POST, request.FILES, instance=request.user.staffprofile)
        if staff_form.is_valid() and staff_profile_form.is_valid():
            staff_form.save()
            staff_profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        staff_form = StaffUpdateForm(instance=request.user)
        staff_profile_form = StaffProfileUpdateForm(instance=request.user.staffprofile)
    context = {
        'staff_form': staff_form,
        'staff_profile_form': staff_profile_form,
    }

    return render(request, 'users/staff_profile.html', context)


@login_required
def stuprofile(request):
    return render(request, 'users/student_profile.html')



class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Authenticate the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            # Check if login is through username/password
            if user.backend == 'django.contrib.auth.backends.ModelBackend':
                # Set a flag indicating login via username/password
                self.request.session['login_method'] = 'username_password'
            else:
                # Set a flag indicating login via other methods (Google OAuth, etc.)
                self.request.session['login_method'] = 'google_oauth'

            login(self.request, user)  # Login the user

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated and 'login_method' in self.request.session:
            if self.request.session['login_method'] == 'username_password':
                return reverse_lazy('MessDeck-staff')  # Redirect to staff dashboard
            else:
                return reverse_lazy('MessDeck-student')  # Redirect to student dashboard

        return reverse_lazy('MessDeck-student')  # Default URL if login method is not identified