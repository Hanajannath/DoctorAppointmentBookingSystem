from django.db import models

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=10,unique=True, blank=True, null=True)
    password = models.CharField(max_length=100,blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
