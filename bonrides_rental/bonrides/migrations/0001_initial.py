# Generated by Django 5.1.3 on 2024-12-01 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(default='Set FName', max_length=50)),
                ('last_name', models.CharField(default='Set LName', max_length=50)),
                ('phone_number', models.CharField(default='Unkown', max_length=15)),
                ('address', models.CharField(default='Unknown Address', max_length=50)),
                ('email', models.EmailField(default='Unkown', max_length=50, unique=True)),
                ('drivers_license_number', models.CharField(default='None', max_length=30)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'permissions': [('can_view_dashboard', 'Can view dashboard'), ('can_manage_users', 'Can manage users')],
            },
        ),
        migrations.CreateModel(
            name='CarBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('car_model', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('rental_date', models.DateField()),
                ('return_date', models.DateField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('model_year', models.PositiveIntegerField()),
                ('brand', models.CharField(max_length=100)),
                ('mileage', models.PositiveIntegerField()),
                ('availability', models.BooleanField(default=True)),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('price', models.PositiveIntegerField(blank=True, default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicle_images/')),
                ('seats', models.PositiveIntegerField(default=1)),
                ('transmission', models.CharField(choices=[('automatic', 'Automatic'), ('manual', 'Manual')], default='manual', max_length=10)),
            ],
        ),
    ]
