from django.db import models

# Create your models here.
class Homepage(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
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
    model = models.CharField(max_length=100)
    model_year = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    mileage = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.model} ({self.model_year}) - {self.registration_number}"