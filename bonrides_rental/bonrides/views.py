from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomUserCreationForm, CarBookingForm, VehicleForm  # Import forms here
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CarBooking, Vehicle  # Import models here

# Create your views here.
def homepage(request):
    context = {}
    return render(request, 'home_page.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def vehicles(request):
    context = {}
    return render(request, 'vehicles.html', context)

def booking(request):
    context = {}
    return render(request, 'booking.html', context)

def contacts(request):
    context = {}
    return render(request, 'contacts.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use email instead of username
        password = request.POST.get('password')
        
        # Authenticate user using email (not username)
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('homepage')  # Redirect to homepage after login
        else:
            messages.info(request, 'Email or Password is incorrect')
    context = {}
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('login')


# Booking Views

def car_booking_list(request):
    bookings = CarBooking.objects.all()
    return render(request, 'car_booking_list.html', {'bookings': bookings})

# Detail view
def car_booking_detail(request, pk):
    booking = get_object_or_404(CarBooking, pk=pk)
    return render(request, 'car_booking_detail.html', {'booking': booking})

# Create view
def car_booking_create(request):
    if request.method == 'POST':
        form = CarBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('car_booking_list')  # Redirect to the booking list after saving
    else:
        form = CarBookingForm()
    return render(request, 'car_booking_form.html', {'form': form})

# Update view
def car_booking_update(request, pk):
    booking = get_object_or_404(CarBooking, pk=pk)
    if request.method == 'POST':
        form = CarBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('car_booking_detail', pk=booking.pk)  # Redirect to the updated booking detail
    else:
        form = CarBookingForm(instance=booking)
    return render(request, 'car_booking_form.html', {'form': form})

# Delete view
def car_booking_delete(request, pk):
    booking = get_object_or_404(CarBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('car_booking_list')  # Redirect to the booking list after deletion
    return render(request, 'car_booking_confirm_delete.html', {'booking': booking})

# Vehicle Views

# Create vehicle
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('manage_vehicles')  # Redirect to the manage vehicles page
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})

# List all vehicles
def manage_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'manage_vehicles.html', {'vehicles': vehicles})

# Update vehicle
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('manage_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'add_vehicle.html', {'form': form})

# Delete vehicle
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('manage_vehicles')
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})
