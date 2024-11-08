from django import forms
from .models import CarBooking  # Ensure you're importing only what you need
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password'
        })


class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['customer_name', 'car_model', 'booking_date', 'rental_duration', 'total_cost']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['model', 'model_year', 'brand', 'mileage', 'availability', 'registration_number']
