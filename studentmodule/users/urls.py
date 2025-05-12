from django.urls import path, include
from django.contrib.auth import views as auth_views
from .import views # Import your custom views if you have them

urlpatterns = [
    # Use Django's built-in LoginView
    # This view expects a template named 'registration/login.html' by default,
    # but you can specify your template using the template_name argument.
    # It handles displaying the form (GET) and processing the login (POST).
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Use Django's built-in LogoutView
    # This view logs the user out and redirects.
    # You might want to specify a template for the logged-out message
    # or a URL to redirect to after logout (controlled by settings.LOGOUT_REDIRECT_URL)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- URL patterns for Password Reset (using Django's built-in views) ---
    # These views handle the multi-step process of password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # --- Placeholder for Signup/Account Request ---
    # You will need a custom view and URL pattern for account requests/signup.
    # path('signup/', views.signup_view, name='signup'), # Example custom view
]
