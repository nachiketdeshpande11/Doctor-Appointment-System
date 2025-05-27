from django.contrib import admin
from .models import Contact,Reviews,Appointment,Patient


# Register your models here.
admin.site.register(Contact)
admin.site.register(Reviews)
admin.site.register(Appointment)
admin.site.register(Patient)
