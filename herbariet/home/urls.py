from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.plant_list, name='plant_list'),
    path('json/', views.api_plants, name='api_plants'),
    # Single route that handles both ID and slug
    path('<str:identifier>/', views.plant_detail, name='plant_detail'),
]