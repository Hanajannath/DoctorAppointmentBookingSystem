from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    specializations = models.ManyToManyField(Specialization)
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    available_days = models.CharField(max_length=100,blank=True, null=True)
    available_time = models.CharField(max_length=50,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    experience = models.PositiveIntegerField(help_text="Years of experience", default=0,null=True,blank=True)
    hospital = models.CharField(max_length=150,null=True,blank=True)
    education = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
         return self.user.get_full_name() or self.user.username