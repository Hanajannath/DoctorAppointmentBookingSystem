from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from doctor.models import Doctor,Specialization
from main.models import ContactMessage
from patient.models import Patient
from appointment.models import Appointment
# Create your views here.

def admin_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'login.html')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def admin_add_doctor(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']

        # Create Django User
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            is_staff=False
        )

        # Create Doctor profile
        Doctor.objects.create(
            user=user,
            name=name,
            available_days=request.POST['available_days'],
            available_time=request.POST['available_time'],
            is_active=True
        )

        return redirect('admin_dashboard')

    return render(request, 'admin_add_doctor.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'dashboard.html', context)

@login_required
def messages_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'messages.html', {'messages': messages})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    return render(request, 'message_detail.html', {'message': message})
@login_required(login_url='admin_login')
def manage_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'manage_doctors.html', {'doctors': doctors})

@login_required(login_url='admin_login')
def add_doctor(request):
    specializations = Specialization.objects.all()
    if request.method == "POST":
        Doctor.objects.create(
            name=request.POST['name'],
            specialization_id=request.POST['specialization'],
            available_days=request.POST['available_days'],
            available_time=request.POST['available_time'],
            image=request.FILES.get('image')
        )
        return redirect('manage_doctors')
    return render(request, 'add_doctor.html',{'specializations':specializations})
@login_required(login_url='admin_login')
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    specializations = Specialization.objects.all()

    if request.method == "POST":
        doctor.name = request.POST['name']
        doctor.available_days = request.POST['available_days']
        doctor.available_time = request.POST['available_time']
        doctor.experience = request.POST['experience']
        doctor.hospital = request.POST['hospital']
        doctor.education = request.POST['education']
        if 'image' in request.FILES:
            doctor.image = request.FILES['image']
        doctor.save()
        spec_ids = request.POST.getlist('specializations')
        doctor.specializations.set(spec_ids)

        return redirect('manage_doctors')

    return render(request, 'edit_doctor.html', {'doctor': doctor,'specializations': specializations})

@login_required(login_url='admin_login')
def block_doctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.is_active = not doctor.is_active
    doctor.save()
    return redirect('manage_doctors')

@login_required(login_url='admin_login')
def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})

@login_required(login_url='admin_login')
def block_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.is_active = not patient.is_active
    patient.save()
    return redirect('view_patients')

@login_required(login_url='admin_login')
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})

@login_required(login_url='admin_login')
def manage_specializations(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        if name:
            if not Specialization.objects.filter(name__iexact=name).exists():
                Specialization.objects.create(name=name)
        return redirect('specializations')
    specializations = Specialization.objects.all()
    return render(request, 'manage_specializations.html', {'specializations': specializations})

@login_required(login_url='admin_login')
def delete_specialization(request, id):
    specialization = get_object_or_404(Specialization, id=id)
    specialization.delete()
    return redirect('specializations')

