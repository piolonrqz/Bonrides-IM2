import json
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomUserCreationForm, CarBookingForm, VehicleForm  # Import forms here
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import CarBooking, User, Vehicle  # Import models here
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

# Create your views here.
def homepage(request):
    context = {}
    return render(request, 'home_page.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def vehicles(request):
    vehicles = Vehicle.objects.filter(availability=True)  # Fetch only available vehicles
    context = {'vehicles': vehicles}
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
            return redirect('login')  # Redirect to login or a success page        else:
        else:
            # Pass only the first error to the context
            for field in form:
                if field.errors:
                    first_error = field.errors[0]
                    break
            return render(request, 'register.html', {'form': form, 'first_error': first_error})
    else:
        form = CustomUserCreationForm()    
        return render(request, 'register.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    user = request.user  # Get the currently logged-in user
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user profile
            return redirect('edit_profile')  # Redirect to the profile page after saving
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

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
            messages.error(request, 'Please correct the errors below.')
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
            messages.error(request, 'Please correct the errors below.')
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
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import VehicleForm
from .models import Vehicle
from django.db import IntegrityError

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VehicleForm
from .models import Vehicle

def add_vehicle(request):
    if not request.user.is_admin:  # Ensure only superusers can access
        return render(request, '404.html')  # If not an admin, raise a 404 error

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')  # Retrieve vehicle ID if editing
        if vehicle_id:
            # Update existing vehicle
            vehicle = get_object_or_404(Vehicle, id=vehicle_id)
            form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        else:
            # Create new vehicle
            form = VehicleForm(request.POST, request.FILES)

        # Check if the form is valid first
        if form.is_valid():
            # Check if registration number already exists (for new vehicles or when updating)
            registration_number = form.cleaned_data.get('registration_number')
            if Vehicle.objects.filter(registration_number=registration_number).exclude(id=vehicle_id if vehicle_id else None).exists():
                form.add_error('registration_number', 'This registration number already exists.')  # Add custom error
                return render(request, 'add_vehicle.html', {'form': form})  # Return the form with the error

            # Save the vehicle
            form.save()

            # Show success message
            messages.success(request, 'Vehicle saved successfully!')

            # Redirect to the same page to clear POST data and ensure a blank form
            return redirect('add_vehicle')

        else:
            # If validation fails, stay on the form page and show the errors
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'add_vehicle.html', {'form': form})  # Render the form with errors

    else:
        form = VehicleForm()
        # If it's a GET request, render the form page
        return render(request, 'add_vehicle.html', {'form': form})



# List all vehicles
def manage_vehicles(request):
    if not request.user.is_admin:  # Ensure only superusers can access
        return render(request, '404.html')  # If not an admin, raise a 404 error
    vehicles = Vehicle.objects.all()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'manage_vehicles.html', {'vehicles': vehicles})
    return render(request, 'manage_vehicles.html', {'vehicles': vehicles})

# Update vehicle
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        # Initialize the form with the `instance` argument to update the existing object
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Vehicle updated successfully!',
                    'vehicle_id': vehicle.pk  # Return the updated vehicle's ID
                })
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('manage_vehicles')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        # When not a POST request, just load the form with the existing instance
        form = VehicleForm(instance=vehicle)
   
    context = {
        'form': form,
        'edit_mode': True,  # Indicate this is edit mode in the template
        'vehicle_id': pk  # Pass the vehicle ID to the template
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'add_vehicle.html', context)
    return render(request, 'add_vehicle.html', context)



# Delete vehicle
@login_required
def delete_vehicle(request, pk):
    # Check if user has staff permissions
    if not request.user.is_staff:
        messages.error(request, 'Unauthorized to delete vehicles')
        return redirect('manage_vehicles')
   
    if request.method == 'POST':
        try:
            vehicle = get_object_or_404(Vehicle, pk=pk)
            vehicle.delete()
            
            # Add a success message
            messages.success(request, 'Vehicle successfully deleted')
            
            return redirect('manage_vehicles')
        
        except Exception as e:
            messages.error(request, f'Error deleting vehicle: {str(e)}')
            return redirect('manage_vehicles')
   
    # For non-POST requests
    messages.error(request, 'Invalid request method')
    return redirect('manage_vehicles')
    
    
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    data = {
        "id": vehicle.id,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "model_year": vehicle.model_year,
        "price": vehicle.price,
        "mileage": vehicle.mileage,
        "seats": vehicle.seats,
        "transmission": vehicle.get_transmission_display(),
        "image": vehicle.image.url if vehicle.image else "",
    }
    return JsonResponse(data)


@login_required
# @staff_member_required  # Decorator ensures only admin (staff) can access
def admin_dashboard(request):
    if not request.user.is_admin:  # Ensure only superusers can access
        return render(request, '404.html')  # If not an admin, raise a 404 error

    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(availability=True).count()
    total_bookings = CarBooking.objects.count()
    active_users = User.objects.filter(active=True).count()  # Changed from is_active to active

    context = {
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'total_bookings': total_bookings,
        'active_users': active_users,
    }
    return render(request, 'admin_dashboard.html', context)

# manage users 

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError


@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
 
from .forms import UserCreationForm  # We'll create this form   
#Create User   
def create_user(request):
    user_id = request.GET.get('user_id')
    if user_id:
        # Editing existing user
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            form = UserCreationForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                # Only update password if provided
                if form.cleaned_data['password1']:
                    user.set_password(form.cleaned_data['password1'])
                # Set role based on selection
                role = form.cleaned_data['role']
                user.staff = role in ['staff', 'admin']
                user.admin = role == 'admin'
                user.save()
                messages.success(request, 'User updated successfully!')
                # return redirect('manage_users')
        else:
            # Initialize form with user data
            initial_data = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'address': user.address,
                'drivers_license_number': user.drivers_license_number,
                'role': 'admin' if user.admin else 'staff' if user.staff else 'user'
            }
            form = UserCreationForm(initial=initial_data, instance=user)
            form.fields['password1'].required = False
            form.fields['password2'].required = False
    else:
        # Creating new user
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                # Set role based on selection
                role = form.cleaned_data['role']
                user.staff = role in ['staff', 'admin']
                user.admin = role == 'admin'
                user.save()
                messages.success(request, 'User created successfully!')
                # return redirect('manage_users')
        else:
            form = UserCreationForm()

    return render(request, 'create_user.html', {'form': form, 'user': user if user_id else None})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm(instance=user)

    return render(request, 'create_user.html', {'form': form, 'user': user})