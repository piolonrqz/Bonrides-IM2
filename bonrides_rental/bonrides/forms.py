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


from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import CarBooking  # Adjust the import based on your project structure

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
        fields = ['model', 'model_year', 'brand', 'mileage', 'availability', 'registration_number', 'price', 'image', 'seats', 'transmission']
