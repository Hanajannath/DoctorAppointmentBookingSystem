from django.shortcuts import render,redirect
from django.contrib import messages
from.models import ContactMessage

# Create your views here.


def main(request):
    return render(request, 'main.html')

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contacts.html')
def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, "All fields are required")
            return redirect('contact')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(request, "Message sent successfully!")
        return redirect('contact')

    return redirect('contact')

def doctors_page(request):
    return render(request, 'doctors.html')

def patients_page(request):
    return render(request, 'patients.html')