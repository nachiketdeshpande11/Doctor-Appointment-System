from django.contrib import admin
from .models import Contact,Reviews,Appointment,Patient, Doctor


# Register your models here.
admin.site.register(Contact)
admin.site.register(Reviews)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Doctor)
