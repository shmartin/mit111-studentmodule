from django.urls import path
from . import views

urlpatterns = [
    path('',views.submission),
    path('guidelines/', views.submission_guidelines, name='submission_guidelines'),
]
