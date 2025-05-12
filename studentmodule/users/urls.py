from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  # Import your custom views if you have them

urlpatterns = [
    # Login view (custom template specified)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Logout view (no changes needed)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset views (built-in Django views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Signup (Account Request) - Add custom view for signup functionality
    path('signup/', views.signup_view, name='signup'),  # Custom view for user registration
]
