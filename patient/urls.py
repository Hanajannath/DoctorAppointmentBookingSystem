"""
URL configuration for Doctorappointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from.import views
from appointment.views import book_appointment 
urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('register/', views.patient_register, name='patient_register'),
    path('patientlogin/', views.patient_login, name='patient_login'),
    path('patientlogout/', views.patient_logout, name='patient_logout'),

    path('viewdoctors/', views.view_doctors, name='view_doctors'),
    path('book/<int:doctor_id>/', book_appointment, name='book_appointment'),

    path('patientappointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path('notifications/', views.patient_notifications, name='patient_notifications'),

]
