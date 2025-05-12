from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Login page
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Password reset page
    path('signup/', views.signup_view, name='signup'),  # Account request page
]
