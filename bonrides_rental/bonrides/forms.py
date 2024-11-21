from django import forms
from .models import CarBooking  # Ensure you're importing only what you need
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle
from .models import User  # Make sure this is importing from your custom User model
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Use your custom User model
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.is_staff is None:  # Ensure is_staff is set
            user.is_staff is None  # or True, based on your logic
        if commit:
            user.save()
        return user
    
User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'drivers_license_number']

    # Optionally add custom widgets for a better UI
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    drivers_license_number = forms.CharField(max_length=20, required=False)

from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import CarBooking

class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['customer_name', 'car_model', 'status', 'rental_date', 'return_date', 'total_cost']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_rental_date(self):
        rental_date = self.cleaned_data.get('rental_date')
        if rental_date <= date.today():
            raise ValidationError("Rental date must be a future date.")
        return rental_date

    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get('rental_date')
        return_date = cleaned_data.get('return_date')

        if rental_date and return_date:
            if return_date <= rental_date:
                raise ValidationError({
                    'return_date': "Return date must be after the rental date."
                })
        return cleaned_data



class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['model', 'model_year', 'brand', 'mileage', 'availability', 'registration_number']
