from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Doctor,Specialization
from appointment.models import *
# Create your views here.
def doctor_login(request):
    error = None

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user and hasattr(user, 'doctor'):
            login(request, user)
            return redirect('doctordashboard')
        else:
            error = "Invalid doctor credentials"

    return render(request, 'doctor_login.html', {'error': error})
def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')

@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
        notifications = Notification.objects.filter(
        doctor=doctor,
        is_read=False
    ).order_by('-created_at')

    except Doctor.DoesNotExist:
        return redirect('doctor_login')

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,'notifications': notifications,
    })

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('doctor_login')
        return view_func(request, *args, **kwargs)
    return wrapper
@doctor_required
def update_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    specializations = Specialization.objects.all()

    if request.method == "POST":
        doctor.name = request.POST['name']
        doctor.available_days = request.POST['available_days']
        doctor.available_time = request.POST['available_time']

        if 'image' in request.FILES:
            doctor.image = request.FILES['image']

        doctor.specializations.set(request.POST.getlist('specializations'))
        doctor.save()

        return redirect('doctordashboard')

    return render(request, 'update_profile.html', {
        'doctor': doctor,
        'specializations': specializations
    })
@doctor_required
def doctor_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor,
        status='Pending'
    ).order_by('appointment_date')

    return render(request, 'doctor_appointments.html', {
        'appointments': appointments
    })
@doctor_required
def update_appointment_status(request, id, status):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointment = get_object_or_404(
        Appointment,
        id=id,
        doctor=doctor
    )

    if status in ['Approved', 'Rejected']:
        appointment.status = status
        appointment.save()

    return redirect('doctor_appointments')
@doctor_required
def appointment_history(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).exclude(status='Pending').order_by('-appointment_date')

    return render(request, 'appointment_history.html', {
        'appointments': appointments
    })

@login_required(login_url='doctor_login')
def doctor_notifications(request):
    doctor = request.user.doctor

    notifications = Notification.objects.filter(
        doctor=doctor
    ).order_by('-created_at')

    return render(request, 'doctor_notifications.html', {
        'notifications': notifications
    })