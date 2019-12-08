from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit),
    path('check/', views.check),
]