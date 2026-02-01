from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment, Notification

@receiver(post_save, sender=Appointment)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Patient notification
        Notification.objects.create(
            patient=instance.patient,
            message=f"Appointment booked with Dr. {instance.doctor.name} "
                    f"on {instance.appointment_date} ({instance.time_slot})"
        )

        # Doctor notification
        Notification.objects.create(
            doctor=instance.doctor,
            message=f"New appointment booked by {instance.patient.name} "
                    f"on {instance.appointment_date} ({instance.time_slot})"
        )
