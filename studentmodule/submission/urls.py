from django.urls import path
from . import views

urlpatterns = [
    path('',views.submission,name='submission'),
    path('guidelines/',views.guidelines,name='guidelines'),
    path('help/', views.help, name='help'),
]
