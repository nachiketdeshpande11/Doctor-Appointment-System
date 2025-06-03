from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from .models import Contact
from .models import Reviews,Appointment,Patient, Doctor
import re
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.db import transaction
import random
from django.utils.timezone import now
from datetime import timedelta


# Create your views here.
def base(request):
    return render(request, 'home.html')

# def contact(request):
#     return render(request, 'contact.html')

@method_decorator(csrf_protect, name='dispatch')
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            mobile = request.POST.get('mobile', '').strip()
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()

            errors = []
            if not name:
                errors.append("Name is required.")
            if not mobile.isdigit() or len(mobile) != 10:
                errors.append("Mobile number must be 10 digits.")
            if "@" not in email or "." not in email:
                errors.append("Email must be valid.")
            if not message:
                errors.append("Message is required.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, self.template_name)

            Contact.objects.create(  
                name=name,
                mobile=mobile,
                email=email,
                message=message
            )

            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')  # ensure 'contact' is a valid URL name

        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return render(request, self.template_name)
    


# def finddoctor(request):
#     return render(request, 'finddoctor.html')

from django.contrib.auth.decorators import login_required
@login_required(login_url='login')  # Redirect to login page if user is not authenticated
def allappointment(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            doctor = request.POST.get('doctor')
            date = request.POST.get('date')

            if not name or not email or not phone or not doctor or not date:
                messages.error(request, "All fields are required.")
                return render(request, 'allappointment.html')

            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                messages.error(request, "Invalid email format.")
                return render(request, 'allappointment.html')

            # Save appointment with logged-in user (if your model supports it)
            Appointment.objects.create(
                # user=request.user,  # Make sure your model has a 'user = models.ForeignKey(User, ...)'
                name=name,
                email=email,
                phone=phone,
                doctor=doctor,
                date=date,
            )

            # Send confirmation email
            subject = 'Appointment Confirmation - DoctorAppointment'
            email_message = f'''
Dear {name},

Your appointment has been successfully booked!

Here are your appointment details:
👨‍⚕️ Doctor: {doctor}  
📅 Date: {date}

Please arrive 10-15 minutes early and bring any relevant medical records with you.

Thank you for choosing DoctorAppointment.  
Stay healthy,  
DoctorAppointment Team
            '''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)

            messages.success(request, "Appointment booked successfully.")
            return redirect('allappointment')

        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, 'allappointment.html')

def viewappointment(request):
    m=Appointment.objects.all()
    context={'data' :m}
    return render(request, 'viewappointment.html',context=context)


def delete(request,mid):
    m=Appointment.objects.filter(id=mid)
    m.delete()
    return redirect('/viewappointment')


def edit(request,mid):
    d={}
    
    m=Appointment.objects.filter(id=mid)
    if request.method=='GET':
        d['data']=m
        return render(request, 'edit.html',d)
    else:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        doctor=request.POST['doctor']
        date= request.POST['date']
        
        
        m_obj=Appointment.objects.filter(id=mid)
        m_obj.update(name=name,email=email,phone=phone,doctor=doctor,date=date)
        messages.success(request, "Appointment updated successfully.")
        return redirect('/viewappointment')

def reviews(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        review = request.POST.get('review')

        if name and email and review:
            Reviews.objects.create(name=name, email=email, review=review)
            messages.success(request, "Thank you for your review!")
            return redirect('reviews')  
        else:
            messages.error(request, "All fields are required.")

    all_reviews = Reviews.objects.all()
    context = {'data': all_reviews}
    return render(request, 'reviews.html', context)

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # --- Input Validation ---
        if not all([full_name, username, dob, gender, contact_number, email, address, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            messages.error(request, "Password must be at least 8 characters and include both letters and numbers.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email or log in.")
            return render(request, 'register.html')

        if Patient.objects.filter(contact_number=contact_number).exists():
            messages.error(request, "Contact number already exists. Please use a different number.")
            return render(request, 'register.html')

        # --- Save to Database (Atomic Block) ---
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = full_name.split(' ')[0] if full_name else ''
                user.last_name = ' '.join(full_name.split(' ')[1:]) if len(full_name.split(' ')) > 1 else ''
                user.save()

                Patient.objects.create(
                    full_name=full_name,
                    username=username,
                    dob=dob,
                    gender=gender,
                    contact_number=contact_number,
                    email=email,
                    address=address
                )

                # Send confirmation email
                subject = 'Welcome to DoctorAppointment - Registration Successful!'
                message = f'''
Dear {full_name},

🎉 Congratulations! You have successfully registered with DoctorAppointment.

Here are your account details:
- Username: {username}
- Email: {email}

You can now log in and book appointments with top doctors.

If you have any questions, feel free to contact our support team.

Stay healthy and take care!

DoctorAppointment Team
                '''
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')

        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist. Please check your unique fields (username, email, contact number).")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip() 
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)
        if user:
           
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('allappointment')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')


# forgot_password functionality
otp_storage = {}
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage[email] = {"otp": otp, "time": now()}

            request.session["reset_email"] = email 

            subject = "Password Reset OTP - DoctorAppointment"
            message = f"""
Hello {user.username},
You requested a password reset. Use the OTP below to proceed:

Your OTP: {otp}

This OTP is valid for 10 minutes.

If you didn't request this, please ignore this email.

Regards,
Ecommerce Team
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            messages.success(request, "OTP has been sent to your email.")
            return redirect("verify_otp")

        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("forgot_password")

    return render(request, "forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        email = request.session.get("reset_email", "").strip().lower()
        otp_entered = request.POST.get("otp")

        if email in otp_storage:
            otp_data = otp_storage[email]

            if now() - otp_data["time"] > timedelta(minutes=10):
                del otp_storage[email]
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect("forgot_password")

            if str(otp_entered) == str(otp_data["otp"]):
                messages.success(request, "OTP verified successfully.")
                return redirect("reset_password")  
            else:
                messages.error(request, "Invalid OTP.")
                return redirect("verify_otp")
        else:
            messages.error(request, "OTP expired or not found. Please try again.")
            return redirect("forgot_password")

    return render(request, "verify_otp.html")

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Validate form inputs
        if not email or not new_password or not confirm_password:
            messages.error(request, "All fields are required!")
            return redirect("reset_password")

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")

        # Validate password complexity
        if len(new_password) < 6 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password):
            messages.error(request, "Password must be at least 6 characters long and contain both letters and numbers.")
            return redirect("reset_password")

        # Try to find the user by email
        try:
            user = User.objects.get(email=email)
        except User.ObjectDoesNotExist:
            messages.error(request, "No account found with the provided email.")
            return redirect("reset_password")

        # Reset the password
        user.set_password(new_password)
        user.save()

        # Provide feedback and redirect
        messages.success(request, "Password reset successful! You can log in now.")
        return redirect("login")

    return render(request, "reset_password.html")


from django.db.models import Q

def srcfilter(request):
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = Doctor.objects.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    else:
        doctors = Doctor.objects.all()

    context = {
        'data': doctors,
        'errmsg': '' if doctors else 'No matching doctors found.'
    }
    return render(request, 'finddoctor.html', context)