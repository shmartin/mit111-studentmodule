from django.urls import path
from . import views

urlpatterns = [
    path('',views.submission),
    path('guidelines/',views.submission),
]