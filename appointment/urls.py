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
from django.contrib import admin
from django.urls import path
from doctor.views import*
from patient.views import*
from.views import*
urlpatterns = [
    path('patient/', patient_notifications, name='patient_notifications'),
    path('doctor/', doctor_notifications, name='doctor_notifications'),
    path('read/<int:id>/', mark_notification_read, name='mark_notification_read'),
    path('notification/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path( 'appointment/receipt/<int:appointment_id>/',appointment_receipt, name='appointment_receipt'),

]
