from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import UserSignupForm
from .models import Users

# Note: For Django's authentication system (authenticate, login, logout)
# to work correctly with your custom Users model, you must set
# AUTH_USER_MODEL = 'your_app_name.Users' in your project's settings.py.
# You might also need a custom authentication backend if you are authenticating
# by email instead of a 'username' field.

# Login view
def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('submission') # Redirect to the submission page

    if request.method == 'POST':
        email = request.POST.get('username') # The login form input name is 'username' but it's for email
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active: # Assuming your Users model has an is_active attribute
                auth_login(request, user) # Log the user in
                messages.success(request, f"Welcome back, {user.firstname}!") # Optional success message
                return redirect('submission') # Redirect to submission page
            else:
                # Handle inactive user account
                messages.error(request, "Your account is inactive.")
        else:
            # Handle invalid credentials
            messages.error(request, "Invalid email or password.")

        # If authentication failed, render the login page again with errors
        # Note: Passing errors via messages is one way; another is to use a Django form
        # for login validation, which handles error display automatically.
        # For simplicity with the current template, we'll pass errors via messages.
        return render(request, 'users/login.html') # Render login page again

    # For GET requests, just render the empty login form
    return render(request, 'users/login.html')

# Logout view
def custom_logout_view(request):
    # Log the user out
    logout(request)
    messages.info(request, "You have been logged out.") # Optional info message
    # Redirect to the login page after logout
    return redirect('login')

# Signup view
def signup_view(request):
    # If the user is already authenticated, redirect them
    if request.user.is_authenticated:
        return redirect('submission') # Redirect to the submission page

    if request.method == 'POST':
        # Instantiate the custom signup form with POST data
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'student' # Example: Assign 'student' role by default
            user.save()

            # Optional: Log the user in automatically after successful signup
            # authenticate() might be needed again depending on your backend
            # user = authenticate(request, email=user.email, password=form.cleaned_data['password'])
            # if user is not None:
            #     auth_login(request, user)
            #     messages.success(request, f"Welcome, {user.firstname}! Your account has been created.")
            #     return redirect('submission')
            # else:
            #     # Handle case where auto-login fails (shouldn't happen if save was successful)
            #     messages.warning(request, "Account created, but automatic login failed. Please log in.")
            #     return redirect('login')

            # Redirect to the login page after successful signup
            messages.success(request, "Your account has been created. Please log in.")
            return redirect('login')
        else:
             # If the form is not valid, errors will be attached to the form object
             # and displayed in the template.
             pass # Form errors will be handled by the template rendering

    else: # For GET requests
        # Instantiate an empty custom signup form
        form = UserSignupForm()

    # Render the signup page with the form (either empty or with errors)
    return render(request, 'users/signup.html', {'form': form})

# Password Reset Views using Django's built-in views
# These views rely on settings.py (AUTH_USER_MODEL) and URL configurations
# to work with your custom user model.

def password_reset_request_view(request):
    return PasswordResetView.as_view(template_name='users/password_reset.html')(request)

def password_reset_done_view(request):
    return PasswordResetDoneView.as_view(template_name='users/password_reset_done.html')(request)

def password_reset_confirm_view(request, uidb64=None, token=None):
    return PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

def password_reset_complete_view(request):
    return PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html')(request)

