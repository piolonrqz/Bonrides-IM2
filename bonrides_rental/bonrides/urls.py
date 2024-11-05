from django.urls import path
from . import views
from .views import (
    car_booking_list,
    car_booking_detail,
    car_booking_create,
    car_booking_update,
    car_booking_delete,
)

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('about/', views.about, name='about'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('booking/', views.booking, name='booking'),
    path('car-bookings/', car_booking_list, name='car_booking_list'),  # Changed to avoid conflict
    path('booking/<int:pk>/', car_booking_detail, name='car_booking_detail'),
    path('booking/new/', car_booking_create, name='car_booking_create'),
    path('booking/<int:pk>/edit/', car_booking_update, name='car_booking_update'),
    path('booking/<int:pk>/delete/', car_booking_delete, name='car_booking_delete'),
]
