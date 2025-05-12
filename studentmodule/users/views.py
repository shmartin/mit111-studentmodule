from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView

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

# Password reset view
def password_reset_view(request):
    return PasswordResetView.as_view()(request)

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})

