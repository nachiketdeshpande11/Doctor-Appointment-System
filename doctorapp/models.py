from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Reviews(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()

    def __str__(self):
        return f"Review by {self.name}"


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    doctor = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"Appointment for {self.name} with {self.doctor} on {self.date} is successful booked!"

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    dob = models.DateField()
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)

    def __str__(self):
        return self.name