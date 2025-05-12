from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('password_reset/', views.password_reset_request_view, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),
    path('signup/', views.signup_view, name='signup'),

    # --- Potential additional URLs based on revue.sql schema ---
    # While the schema doesn't require specific URLs, you might add URLs
    # to manage user data beyond basic authentication, e.g., viewing user profiles.

    # Example: URL to view details of a specific user (using the user's uid from the schema)
    # path('users/<int:uid>/', views.user_detail, name='user_detail'),

    # Example: URL to edit a user's profile
    # path('users/<int:uid>/edit/', views.user_edit, name='user_edit'),
]
