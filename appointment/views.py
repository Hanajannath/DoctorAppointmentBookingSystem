from django.shortcuts import render,redirect,get_object_or_404
from .utils import slot_within_doctor_time,is_past_time
from .models import Appointment
from doctor.models import Doctor
# Create your views here.
from django.db.models import Count
from datetime import date
from .models import Notification
from doctor.models import *
from patient .models import*



MAX_PATIENTS_PER_SLOT = 8

def book_appointment(request, doctor_id):
    if 'patient_id' not in request.session:
        return redirect('patient_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    selected_date = request.GET.get('date') or request.POST.get('date')
    booked_slots = {}

    # 🔢 Count bookings per slot (IMPORTANT FIX)
    if selected_date:
        slot_data = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=selected_date,
            status__in=['Pending', 'Approved']
        ).values('time_slot').annotate(count=Count('id'))

        booked_slots = {s['time_slot']: s['count'] for s in slot_data}

    if request.method == "POST":
        selected_slot = request.POST.get('time_slot')

        # ❌ Missing input
        if not selected_date or not selected_slot:
            return render(request, 'book_appointment.html', {
                'doctor': doctor,
                'booked_slots': booked_slots,
                'error': 'Please select date and time slot.'
            })

        # ❌ Past date
        if date.fromisoformat(selected_date) < date.today():
            return render(request, 'book_appointment.html', {
                'doctor': doctor,
                'booked_slots': booked_slots,
                'error': 'You cannot book for a past date.'
            })
        # ❌ Past time check (today only)
        if selected_date == date.today().isoformat():
            if is_past_time(selected_date, selected_slot):
                return render(request, 'book_appointment.html', {
                    'doctor': doctor,
                    'booked_slots': booked_slots,
                    'error': 'You cannot book a past time slot.'
                })

        # ❌ Outside doctor working hours
        if not slot_within_doctor_time(selected_slot, doctor.available_time):
            return render(request, 'book_appointment.html', {
                'doctor': doctor,
                'booked_slots': booked_slots,
                'error': 'Selected time slot is outside doctor working hours.'
            })
        # ❌ Same patient booking same slot again
        already_booked = Appointment.objects.filter(
            patient_id=request.session['patient_id'],
            doctor=doctor,
            appointment_date=selected_date,
            time_slot=selected_slot,
            status__in=['Pending', 'Approved']
        ).exists()

        if already_booked:
            return render(request, 'book_appointment.html', {
                'doctor': doctor,
                'booked_slots': booked_slots,
                'error': 'You already booked this time slot.'
            })

        # ❌ Slot full (8 patients)
        if booked_slots.get(selected_slot, 0) >= MAX_PATIENTS_PER_SLOT:
            return render(request, 'book_appointment.html', {
                'doctor': doctor,
                'booked_slots': booked_slots,
                'error': 'This time slot is full. Please choose another slot.'
            })
        
        # ✅ Save appointment
        Appointment.objects.create(
            patient_id=request.session['patient_id'],
            doctor=doctor,
            appointment_date=selected_date,
            time_slot=selected_slot
        )

        return redirect('my_appointments')

    return render(request, 'book_appointment.html', {
        'doctor': doctor,
        'booked_slots': booked_slots
    })

def mark_notification_read(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.is_read = True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
from django.shortcuts import get_object_or_404, redirect

def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from .models import Appointment

def appointment_receipt(request, appointment_id):
    appointment = Appointment.objects.get(
        id=appointment_id,
        patient_id=request.session['patient_id']
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Appointment_Receipt_{appointment.id}.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ---- Header ----
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 80, "Appointment Receipt")

    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 110, "Doctor Appointment System")

    # ---- Content ----
    y = height - 180
    line_gap = 25

    def draw(label, value):
        nonlocal y
        p.drawString(80, y, f"{label}:")
        p.drawString(250, y, str(value))
        y -= line_gap

    draw("Receipt No", appointment.id)
    draw("Patient Name", appointment.patient.name)
    draw("Doctor Name", appointment.doctor.name)
    draw("Appointment Date", appointment.appointment_date)
    draw("Time Slot", appointment.time_slot)
    draw("Status", appointment.status)
    draw("Booked On", appointment.created_at.strftime("%d-%m-%Y %I:%M %p"))

    # ---- Footer ----
    p.drawString(80, y - 40, "Thank you for booking your appointment.")
    p.drawString(80, y - 60, "Please keep this receipt for reference.")

    p.showPage()
    p.save()

    return response
