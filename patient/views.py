from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientRegisterForm, PatientLoginForm
from doctor.models import Doctor, Specialization
from appointment.models import *
from django.contrib.auth.hashers import check_password




# Create your views here.
def patient_dashboard(request):
    patient_id = request.session.get('patient_id')

    notifications = Notification.objects.filter(
        patient_id=patient_id,
        is_read=False
    ).order_by('-created_at')

    return render(request, 'patient_dashboard.html', {
        'notifications': notifications,
    })
def patient_register(request):
    form = PatientRegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('patient_login')

    return render(request, 'register.html', {'form': form})


def patient_login(request):
    form = PatientLoginForm(request.POST or None)
    error = None

    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(name=name)

            if not patient.is_active:
                error = "Your account is blocked by admin"

            elif check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                request.session['patient_name'] = patient.name
                return redirect('patient_dashboard')

            else:
                error = "Invalid name or password"

        except Patient.DoesNotExist:
            error = "Invalid name or password"

    return render(request, 'patientlogin.html', {
        'form': form,
        'error': error
    })
def patient_logout(request):
    request.session.flush()
    return redirect('patient_login')
def view_doctors(request):
    doctors = Doctor.objects.filter(is_active=True)
    specializations = Specialization.objects.all()

    spec_id = request.GET.get('specialization')
    if spec_id:
        doctors = doctors.filter(specializations__id=spec_id)

    return render(request, 'view_doctor.html', {
        'doctors': doctors,
        'specializations': specializations
    })

def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient_id=request.session['patient_id']
    ).order_by('-appointment_date')

    return render(request, 'my_appointments.html', {
        'appointments': appointments
    })
def cancel_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id)

    if request.method == "POST" and appt.status == 'Pending':
        appt.status = 'Cancelled'
        appt.save()
        return redirect('my_appointments')

    return render(request, 'cancel_appointments.html', {'appointment': appt})
def patient_notifications(request):
    patient = Patient.objects.get(id=request.session['patient_id'])

    notifications = Notification.objects.filter(
        patient=patient
    ).order_by('-created_at')

    return render(request, 'patient_notifications.html', {
        'notifications': notifications
    })