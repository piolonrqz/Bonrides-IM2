from django.urls import path
from django.conf.urls import handler404
from bonrides.views import custom_404
from . import views
from .views import (
    car_booking_list,
    car_booking_detail,
    car_booking_create,
    car_booking_update,
    car_booking_delete,
    edit_user,
    delete_user,
)

handler404 = custom_404

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('about/', views.about, name='about'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('booking/', views.booking, name='booking'),
    path('admin-dashboard/car-bookings/', car_booking_list, name='car_booking_list'),  # Changed to avoid conflict
    path('booking/<int:pk>/', car_booking_detail, name='car_booking_detail'),
    path('booking/new/', car_booking_create, name='car_booking_create'),
    path('booking/<int:pk>/edit/', car_booking_update, name='car_booking_update'),
    path('booking/<int:pk>/delete/', car_booking_delete, name='car_booking_delete'),
    path('admin-dashboard/vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('admin-dashboard/vehicles/manage/', views.manage_vehicles, name='manage_vehicles'),
    path('admin-dashboard/vehicles/edit/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('admin-dashboard/vehicles/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('vehicle-details/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]
