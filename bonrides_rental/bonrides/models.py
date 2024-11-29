from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name='', last_name='', phone_number='', address='', drivers_license_number='', is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            drivers_license_number=drivers_license_number
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = True
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password=None, first_name='', last_name='', phone_number='', address='', drivers_license_number=''):
        return self.create_user(email, password, first_name, last_name, phone_number, address, drivers_license_number, is_staff=True)
    
    def create_superuser(self, email, password=None, first_name='', last_name='', phone_number='', address='', drivers_license_number=''):
        return self.create_user(email, password, first_name, last_name, phone_number, address, drivers_license_number, is_staff=True, is_admin=True)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)# Custom User Model
    
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, default="Set FName")
    last_name = models.CharField(max_length=50, default="Set LName")
    phone_number = models.CharField(max_length=15, default="Unkown")
    address = models.CharField(max_length=50, default="Unknown Address")
    email = models.EmailField(max_length=50, unique=True, default="Unkown")
    drivers_license_number = models.CharField(max_length=30, default="None")
    
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # super user
    timestamp = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'  # email is used as username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # These fields are required when creating a superuser
    
    objects = UserManager()  # Use your custom user manager
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_manage_users", "Can manage users"),
        ]
    
class CarBooking(models.Model):
    customer_name = models.CharField(max_length=200)
    car_model = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    rental_date = models.DateField()
    return_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer_name} - {self.car_model}"
class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    model = models.CharField(max_length=100)
    model_year = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    mileage = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    seats = models.PositiveIntegerField(default=1)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='manual')

    def __str__(self):
        return f"{self.model} ({self.model_year}) - {self.registration_number}"