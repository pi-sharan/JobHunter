
from django.urls import path
from .import views

urlpatterns = [
    # Recommend Route
    path('recommend/', views.recommend, name = 'recommend'),
]