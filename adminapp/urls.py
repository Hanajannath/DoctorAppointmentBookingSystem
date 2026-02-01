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
from . import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('registeradd-doctor/', views.admin_add_doctor, name='admin_add_doctor'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('messages/', views.messages_list, name='admin_messages'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('add/',views.add_doctor,name='add_doctors'),
    path('edit/<int:id>/',views.edit_doctor,name='edit_doctor'),
    path('block/<int:id>/',views.block_doctor,name='block_doctor'),

    path('patients/', views.view_patients, name='view_patients'),
    path('blockpatients/<int:id>/',views.block_patient,name='blockpatient'),

    path('appointments/', views.view_appointments, name='manage_appointments'),

    path('specializations/',views.manage_specializations,name='specializations'),
    path('specialization/delete/<int:id>/', views.delete_specialization, name='delete_specialization'),

    path('logout/', views.admin_logout, name='admin_logout'),
]


