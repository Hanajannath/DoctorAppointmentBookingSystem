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
from.views import*
urlpatterns = [
   
    path('', main, name='main'),
    path('home/', home, name='home'),
    path('about/', about,name='about'),
    path('contact/',contact,name='contact'),
    path('send/',send_message, name='send_message'),
    path('doctorspage/',doctors_page,name='doctorspage'),
    path('patientspage/',patients_page,name='patientspage'),
]


