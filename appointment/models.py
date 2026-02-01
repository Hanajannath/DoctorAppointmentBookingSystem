from django.db import models

# Create your models here.

from doctor.models import Doctor
from patient.models import Patient
from django.core.exceptions import ValidationError

def save(self, *args, **kwargs):
    count = Appointment.objects.filter(
        doctor=self.doctor,
        appointment_date=self.appointment_date,
        time_slot=self.time_slot,
        status__in=['Pending', 'Approved']
    ).count()

    if count >= 8:
        raise ValidationError("This time slot is already full.")

    super().save(*args, **kwargs)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    ]
    SLOT_CHOICES = [
        ('09-10', '09:00 - 10:00'),
        ('10-11', '10:00 - 11:00'),
        ('11-12', '11:00 - 12:00'),
        ('14-15', '02:00 - 03:00'),
        ('15-16', '03:00 - 04:00'),
        ('16-17', '04:00 - 05:00'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    appointment_date = models.DateField(null=True,blank=True)
    time_slot = models.CharField(max_length=20, choices=SLOT_CHOICES,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor', 'appointment_date', 'time_slot'],
                name='unique_patient_slot'
            )
        ]
    def __str__(self):
        return f"{self.patient} - {self.doctor}"


class Notification(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
