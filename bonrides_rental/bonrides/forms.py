from django import forms
from .models import CarBooking  # Ensure you're importing only what you need
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle
from .models import User  # Make sure this is importing from your custom User model
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email:'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password:'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password:'})
    )
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.is_staff is None:  # Ensure is_staff is set
            user.is_staff = None  # or True, based on your logic
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
    # address = forms.CharField(widget=forms.Textarea, required=False) // temporarily disable
    drivers_license_number = forms.CharField(max_length=20, required=True)
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
        fields = ['model', 'model_year', 'brand', 'mileage', 'availability', 'registration_number', 'price', 'image', 'seats', 'transmission']

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
class UserCreationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    # Existing fields remain the same
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    drivers_license_number = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Add the role selection field
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'drivers_license_number', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If editing existing user, make passwords optional
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Only validate passwords if at least one is provided
        if password1 or password2:
            if not password1 or not password2:
                raise forms.ValidationError("Both password fields must be filled out")
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data
