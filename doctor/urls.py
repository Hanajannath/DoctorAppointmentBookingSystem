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
from.import views
urlpatterns = [
      path('login/', views.doctor_login, name='doctor_login'),
      path('logout/', views.doctor_logout, name='doctor_logout'),
      path(' drdashboard/',views.doctor_dashboard,name='doctordashboard'),
      path('profile/', views.update_profile, name='doctor_profile'),
      path('drappointments/',views.doctor_appointments,name='doctor_appointments'),
      path('appointments/update/<int:id>/<str:status>/',views.update_appointment_status, name='update_appointment_status'),
      path('appointments/history/', views.appointment_history, name='appointment_history'),
      path('notifications/', views.doctor_notifications, name='doctor_notifications'),

]
