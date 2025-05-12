from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import UserSignupForm  # Import the custom signup form

# Login view
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('submission')  # Redirect to submission page
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'users/login.html')

# Logout view
def custom_logout_view(request):
    logout(request)
    return redirect('login')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)  # Use the custom signup form
        if form.is_valid():
            user = form.save(commit=False)  # Do not save to DB yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Now save to DB
            auth_login(request, user)  # Automatically log in the user after signup
            return redirect('submission')  # Redirect to the submission page
    else:
        form = UserSignupForm()  # Initialize the form
    
    return render(request, 'users/signup.html', {'form': form})

# Password Reset View
def password_reset_request_view(request):
    return PasswordResetView.as_view(template_name='users/password_reset.html')(request)

def password_reset_done_view(request):
    return PasswordResetDoneView.as_view(template_name='users/password_reset_done.html')(request)

def password_reset_confirm_view(request, uidb64=None, token=None):
    return PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

def password_reset_complete_view(request):
    return PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html')(request)
