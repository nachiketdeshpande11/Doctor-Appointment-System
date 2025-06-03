from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),

    path('allappointment/',views.allappointment, name='allappointment'),
    path('edit/<int:mid>/', views.edit, name='edit'),
    path('delete/<int:mid>/', views.delete, name='delete'),
    path('viewappointment/', views.viewappointment, name='viewappointment'),
    
    path('reviews/',views.reviews, name='reviews'),
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/',views.reset_password,name='reset_password'),
 
    path('finddoctor/', views.srcfilter, name='srcfilter'),
]
